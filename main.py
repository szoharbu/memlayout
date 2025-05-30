#!/usr/bin/env python3
"""
memlayout - Memory Layout Library Demo

This demonstrates the core interval allocation functionality.
"""

from memlayout.page_table_management.page_table_manager import get_page_table_manager
from memlayout.utils.enums import Execution_context


def main():
    """Main demonstration function"""
    print("🚀 memlayout - Memory Layout Library Demo")
    print("=" * 60)
    
    page_table_manager = get_page_table_manager()

    # for core in ["core_0", "core_1"]:
    #     page_table_manager.create_mmu(mmu_name=f"{core}_el1_NS", execution_context=Execution_context.EL1_NS)
    
    print("✅ Successfully imported get_page_table_manager!")
    print("✅ Page table manager initialized!")

if __name__ == "__main__":
    main() 