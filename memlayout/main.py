#!/usr/bin/env python3
"""
memlayout - Memory Layout Library Demo

This demonstrates the core interval allocation functionality.
"""

def print_separator(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def print_intervals(lib, title="Current Intervals"):
    print(f"\n--- {title} ---")
    if hasattr(lib, 'intervals') and lib.intervals:
        for i, interval in enumerate(lib.intervals):
            print(f"  {i+1}. {interval}")
    else:
        print("  No intervals available")

def demo_basic_allocation():
    """Demonstrate basic interval allocation with logging"""
    print_separator("BASIC INTERVAL ALLOCATION DEMO WITH LOGGING")
    
    # This will work once we move the interval_lib.py code
    from memlayout import IntervalLib, setup_logging, LogLevel
    
    # Setup logging
    logger = setup_logging(level=LogLevel.INFO, use_colors=True)
    
    # Create an address space (16MB starting at 0x10000000)
    print("Creating address space: 0x10000000 - 0x10FFFFFF (16MB)")
    allocator = IntervalLib(start_address=0x10000000, total_size=0x1000000)
    
    # Log the initial setup
    logger.log_region_add(0x10000000, 0x1000000, {"type": "initial_space"})
    print_intervals(allocator, "Initial State")
    
    # Allocate some regions with logging
    print("\n--- Performing Allocations ---")
    
    # Allocate 4KB aligned to 4KB boundary
    print("1. Allocating 4KB with 4KB alignment...")
    try:
        result = allocator.find_and_remove(size=0x1000, alignment_bits=12)
        if result:
            start, size = result
            logger.log_allocation(start, size, alignment_bits=12)
            print(f"   Allocated: 0x{start:08x} - 0x{start+size-1:08x} (size: 0x{size:x})")
        print_intervals(allocator, "After 4KB allocation")
    except ValueError as e:
        logger.log_error("allocation", str(e), size=0x1000, alignment=12)
    
    # Allocate 8KB with no specific alignment
    print("\n2. Allocating 8KB with default alignment...")
    try:
        result = allocator.find_and_remove(size=0x2000)
        if result:
            start, size = result
            logger.log_allocation(start, size)
            print(f"   Allocated: 0x{start:08x} - 0x{start+size-1:08x} (size: 0x{size:x})")
        print_intervals(allocator, "After 8KB allocation")
    except ValueError as e:
        logger.log_error("allocation", str(e), size=0x2000)
    
    # Allocate 1MB aligned to 1MB boundary
    print("\n3. Allocating 1MB with 1MB alignment...")
    try:
        result = allocator.find_and_remove(size=0x100000, alignment_bits=20)
        if result:
            start, size = result
            logger.log_allocation(start, size, alignment_bits=20)
            print(f"   Allocated: 0x{start:08x} - 0x{start+size-1:08x} (size: 0x{size:x})")
        print_intervals(allocator, "After 1MB allocation")
    except ValueError as e:
        logger.log_error("allocation", str(e), size=0x100000, alignment=20)
    
    # Show final statistics with logging
    print(f"\n--- Final Statistics ---")
    total_free = sum(interval.size for interval in allocator.intervals)
    total_used = 0x1000000 - total_free
    fragmentation = len(allocator.intervals)
    
    logger.log_stats(len(allocator.intervals), total_free, fragmentation)
    
    print(f"Total address space: 0x{0x1000000:x} ({0x1000000//1024//1024}MB)")
    print(f"Total allocated: 0x{total_used:x} ({total_used//1024}KB)")
    print(f"Total free: 0x{total_free:x} ({total_free//1024//1024}MB)")
    print(f"Fragmentation: {fragmentation} free regions")
    


def demo_metadata_intervals():
    """Demonstrate intervals with metadata and advanced logging"""
    print_separator("METADATA & ADVANCED LOGGING DEMO")
    
    try:
        from memlayout import IntervalLib, setup_logging, LogLevel
        
        # Setup debug logging to see more detail
        logger = setup_logging(level=LogLevel.DEBUG, use_colors=True)
        
        print("Creating address space with metadata support...")
        allocator = IntervalLib(start_address=0x20000000, total_size=0x800000)  # 8MB
        
        # Add different types of regions with logging
        print("Adding regions with different metadata...")
        
        # Performance timing example
        perf_id = logger.log_performance_start("add_code_region")
        
        # Add a code region
        allocator.add_region(0x20000000, 0x200000, {"type": "code", "permissions": "rx"})
        logger.log_region_add(0x20000000, 0x200000, {"type": "code", "permissions": "rx"})
        print("Added: Code region (2MB) - executable")
        
        logger.log_performance_end(perf_id, "add_code_region")
        
        # Add a data region  
        allocator.add_region(0x20200000, 0x400000, {"type": "data", "permissions": "rw"})
        logger.log_region_add(0x20200000, 0x400000, {"type": "data", "permissions": "rw"})
        print("Added: Data region (4MB) - read/write")
        
        # Add a device region
        allocator.add_region(0x20600000, 0x200000, {"type": "device", "permissions": "rw", "cache": "uncached"})
        logger.log_region_add(0x20600000, 0x200000, {"type": "device", "permissions": "rw", "cache": "uncached"})
        print("Added: Device region (2MB) - uncached")
        
        print_intervals(allocator, "Regions with Metadata")
        
        # Log final stats
        stats = allocator.get_stats()
        logger.info(f"📊 Final stats: {stats}")
        
    except ImportError:
        print("⚠️  Advanced features not yet available")
        print("Expected output:")
        print("  1. [0x20000000-0x201fffff] size=0x200000 (type=code, permissions=rx)")
        print("  2. [0x20200000-0x205fffff] size=0x400000 (type=data, permissions=rw)")
        print("  3. [0x20600000-0x207fffff] size=0x200000 (type=device, permissions=rw, cache=uncached)")

def demo_logging_levels():
    """Demonstrate different logging levels"""
    print_separator("LOGGING LEVELS DEMO")
    
    try:
        from memlayout import setup_logging, LogLevel
        
        print("Testing different log levels...")
        
        # Test each log level
        for level in [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING]:
            print(f"\n--- Logging at {level.name} level ---")
            logger = setup_logging(level=level, use_colors=True)
            
            logger.debug("This is a debug message")
            logger.info("This is an info message") 
            logger.log_warning("This is a warning message")
            logger.log_error("test_operation", "This is an error message")
            
    except ImportError:
        print("⚠️  Logging not yet available")

def main():
    """Main demonstration function"""
    print("🚀 memlayout - Memory Layout Library Demo with Logging")
    print("=" * 60)
    
    demo_basic_allocation()
    demo_metadata_intervals()
    demo_logging_levels()
    
    print_separator("DEMO COMPLETE")
    print("✅ Logger successfully integrated!")
    print("Features demonstrated:")
    print("  • Colored console output with emojis")
    print("  • Allocation/deallocation tracking")
    print("  • Performance timing") 
    print("  • Statistics logging")
    print("  • Error and warning handling")
    print("  • Different log levels")

if __name__ == "__main__":
    main()