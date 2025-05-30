#!/usr/bin/env python3
"""
memlayout - Memory Layout Library Demo

This demonstrates the core interval allocation functionality.
"""

import random
from memlayout.page_table_management.page_table_manager import get_page_table_manager
from memlayout.utils.enums import Execution_context, Page_sizes, Page_types
from memlayout.utils.logger import setup_logging, LogLevel


def main():
    """Main demonstration function"""
    # Setup logging FIRST - before any other operations
    logger = setup_logging(level=LogLevel.INFO, show_timestamp=True)
    
    logger.info("🚀 memlayout - Memory Layout Library Demo")
    logger.info("=" * 60)
    
    logger.info("Initializing page table manager...")
    page_table_manager = get_page_table_manager()

    for core in ["core_0", "core_1"]:
        el3r = page_table_manager.create_page_table(page_table_name=f"{core}_el3_root", core_id=core, execution_context=Execution_context.EL3)

        # #Always allocate a code page table that has a VA=PA mapping, needed for BSP boot block
        # el3r.allocate_page(size=Page_sizes.SIZE_2M, page_type=Page_types.TYPE_CODE, sequential_page_count=1, VA_eq_PA=True)

        # for type in [Page_types.TYPE_CODE, Page_types.TYPE_DATA]:
        #     count = random.randint(6, 8)
        #     for _ in range(count):
        #         sequential_page_count = choice(values={1:90, 2:9, 3:1})
        #         size = random.choice([Page_sizes.SIZE_4K, Page_sizes.SIZE_2M])
        #         el3r.allocate_page(size=size, page_type=type, sequential_page_count=sequential_page_count)


    
    logger.info("✅ Successfully run memlayout demo")

if __name__ == "__main__":
    main() 