#!/usr/bin/env python3
"""
memlayout - Memory Layout Library Demo

This demonstrates the core interval allocation functionality.
"""

import random
from memlayout.page_table_management.page_table_manager import get_page_table_manager
from memlayout.utils.enums import Execution_context, Page_sizes, Page_types
from memlayout.utils.logger import setup_logging, LogLevel, get_logger


def init_page_tables():

    page_table_manager = get_page_table_manager()

    logger = get_logger()
    for core in ["core_0", "core_1"]:
        # NOTE: Must create the page tables first before allocating pages
        page_table_manager.create_page_table(page_table_name=f"{core}_el3_root", core_id=core, execution_context=Execution_context.EL3)
        page_table_manager.create_page_table(page_table_name=f"{core}_el1_ns", core_id=core, execution_context=Execution_context.EL1_NS)

    page_tables = page_table_manager.get_all_page_tables()

    # Allocate a cross-core page table from a random page table. preferably to allocate the cross-core page table first to avoid conflicts
    page_table_i = page_tables[0]
    page_table_i.allocate_cross_core_page()

    for page_table in page_tables:
        logger.info(f"Core: {page_table.core_id} Page Table: {page_table.page_table_name}")
        if page_table.execution_context == Execution_context.EL3:
            #Always allocate a code page table that has a VA=PA mapping, needed for BSP boot block
            page_table.allocate_page(size=Page_sizes.SIZE_2M, page_type=Page_types.TYPE_CODE, sequential_page_count=1, VA_eq_PA=True)

        for type in [Page_types.TYPE_CODE, Page_types.TYPE_DATA]:
            count = random.randint(6, 8)
            for _ in range(count):
                #sequential_page_count = choice(values={1:90, 2:9, 3:1})
                sequential_page_count = random.choices(population=[1, 2, 3], weights=[90, 9, 1], k=1)
                size = random.choice([Page_sizes.SIZE_4K, Page_sizes.SIZE_2M])
                page_table.allocate_page(size=size, page_type=type, sequential_page_count=sequential_page_count[0])

def init_segments():
    logger = get_logger()
    logger.info("======== init_segments")
    page_table_manager = get_page_table_manager()
    page_tables = page_table_manager.get_all_page_tables()


    core_0_el3_page_table = next(page_table for page_table in page_tables if page_table.core_id == "core_0" and page_table.execution_context == Execution_context.EL3)
    # Allocate BSP boot segment. a single segment that act as trampoline for all cores
    bsp_boot_segment = core_0_el3_page_table.allocate_memory_segment(page_table=core_0_el3_page_table,
                                                                    name=f"BSP__boot_segment", 
                                                                    byte_size=0x200,
                                                                    memory_type=Memory_types.BSP_BOOT_CODE, 
                                                                    alignment_bits=4, 
                                                                    VA_eq_PA=True)
    logger.debug(f"============ init_segments: allocated BSP_boot_segment {bsp_boot_segment}")

    # Allocating one cross-core page, ensuring that all core and all MMUs will have one shared PA space
    # This allocation is done here, as it is needed for all cores, and should be done before any other allocation to avoid conflicts
    cross_page_segment = core_0_el3_page_table.segment_manager.allocate_cross_core_data_memory_segment()
    logger.debug(f"============ init_segments: allocated cross_page_segment {cross_page_segment}")


    for page_table in page_tables:
        logger.info(f"Core: {page_table.core_id} Page Table: {page_table.page_table_name}")
        logger.info(f"================ init_segments: {page_table.page_table_name}")

        if page_table.core_id == "core_0":
            # Allocate BSP boot segment. a single segment that act as trampoline for all cores
            EL3_mmu = next(mmu for mmu in curr_state.enabled_mmus if mmu.execution_context == Configuration.Execution_context.EL3)
            bsp_boot_segment = curr_state.segment_manager.allocate_memory_segment(mmu=EL3_mmu,
                                                                            name=f"BSP__boot_segment", 
                                                                            byte_size=0x200,
                                                                            memory_type=Configuration.Memory_types.BSP_BOOT_CODE, 
                                                                            alignment_bits=4, 
                                                                            VA_eq_PA=True)
            logger.debug(f"init_memory: allocated BSP_boot_segment {bsp_boot_segment}")

            # Allocating one cross-core page, ensuring that all core and all MMUs will have one shared PA space
            # This allocation is done here, as it is needed for all cores, and should be done before any other allocation to avoid conflicts
            cross_page_segment = curr_state.segment_manager.allocate_cross_core_data_memory_segment()
            logger.debug(f"init_memory: allocated cross_page_segment {cross_page_segment}")

        core_mmus = mmu_manager.get_core_mmus(state_name)

        for mmu in core_mmus:
            # allocating one boot_segment for each of the states EL3 MMUs
            if mmu.execution_context == Configuration.Execution_context.EL3:
                boot_segment = curr_state.segment_manager.allocate_memory_segment(mmu=mmu, 
                                                                            name=f"{state_name}__boot_segment",
                                                                            byte_size=0x200,
                                                                            memory_type=Configuration.Memory_types.BOOT_CODE, 
                                                                            alignment_bits=4, 
                                                                            VA_eq_PA=True)
                logger.debug(f"init_memory: allocating boot_segment {boot_segment} for {state_name}:{mmu.mmu_name}")

            code_segment_count = Configuration.Knobs.Memory.code_segment_count.get_value()
            for i in range(code_segment_count):
                code_segment = curr_state.segment_manager.allocate_memory_segment(mmu=mmu,
                                                                            name=f"{state_name}__code_segment_{i}",
                                                                            byte_size=0x1000,
                                                                            memory_type=Configuration.Memory_types.CODE, 
                                                                            alignment_bits=4)
                logger.debug(f"init_memory: allocating code_segment {code_segment} for {state_name}:{mmu.mmu_name}")

            data_segment_count = Configuration.Knobs.Memory.data_segment_count.get_value()
            data_shared_count = data_segment_count // 2  # First part is half of n (floored)
            data_preserve_count = data_segment_count - data_shared_count  # Second part is the remainder
            for i in range(data_shared_count):
                data_segment = curr_state.segment_manager.allocate_memory_segment(mmu=mmu,
                                                                            name=f"{state_name}__data_shared_segment_{i}",
                                                                            byte_size=0x1000,
                                                                            alignment_bits=4,
                                                                            memory_type=Configuration.Memory_types.DATA_SHARED)
                logger.debug(f"init_memory: allocating data_shared_segment {data_segment} for {state_name}:{mmu.mmu_name}")

            for i in range(data_preserve_count):
                data_segment = curr_state.segment_manager.allocate_memory_segment(mmu=mmu,
                                                                            name=f"{state_name}__data_preserve_segment_{i}", 
                                                                            byte_size=0x1000,
                                                                            alignment_bits=4,
                                                                            memory_type=Configuration.Memory_types.DATA_PRESERVE)
                logger.debug(f"init_memory: allocating data_preserve_segment {data_segment} for {state_name}:{mmu.mmu_name}")

            # Allocate stack space for each of the MMUs
            stack_segment = curr_state.segment_manager.allocate_memory_segment(mmu=mmu,
                                                                            name=f"{state_name}__stack_segment",
                                                                            byte_size=0x800,
                                                                            alignment_bits=4,
                                                                            memory_type=Configuration.Memory_types.STACK)
            logger.debug(f"init_memory: allocating stack_segment {stack_segment} for {state_name}:{mmu.mmu_name}")

    state_manager.set_active_state("core_0")
            
def main():
    """Main demonstration function"""
    # Setup logging FIRST - before any other operations
    logger = setup_logging(level=LogLevel.INFO, show_timestamp=True)
    
    logger.info("🚀 memlayout - Memory Layout Library Demo")
    logger.info("=" * 60)
    
    logger.info("Initializing page table manager...")
    page_table_manager = get_page_table_manager()

    logger.info("Initializing page tables...")
    init_page_tables()

    logger.info("Initializing segments...")
    init_segments()

    logger.info("Printing page table manager...")
    # Print the page table manager
    page_table_manager.print_memory_summary()

    logger.info("✅ Successfully run memlayout demo")

if __name__ == "__main__":
    main() 

