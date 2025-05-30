#!/usr/bin/env python3
"""
Basic tests for memlayout library
"""
from memlayout import Interval, IntervalLib

def test_import():
    """Test that we can import the library"""
    try:
        import memlayout
        print("✓ Successfully imported memlayout")
        return True
    except ImportError as e:
        print(f"✗ Failed to import memlayout: {e}")
        return False

def test_interval_lib():
    """Test basic IntervalLib functionality"""
    try:
        from memlayout import IntervalLib
        
        # Create a simple allocator
        allocator = IntervalLib(start_address=0x1000, total_size=0x10000)
        print("✓ Created IntervalLib instance")
        
        # Test basic allocation
        result = allocator.find_and_remove(size=0x1000, alignment_bits=12)
        if result:
            start, size = result
            print(f"✓ Allocated region: 0x{start:x} (size: 0x{size:x})")
        else:
            print("✗ Failed to allocate region")
            return False
            
        # Check remaining intervals
        if hasattr(allocator, 'intervals') and allocator.intervals:
            remaining = sum(interval.size for interval in allocator.intervals)
            expected = 0x10000 - 0x1000  # Original size minus allocated
            if remaining == expected:
                print(f"✓ Correct remaining space: 0x{remaining:x}")
            else:
                print(f"✗ Incorrect remaining space: 0x{remaining:x} (expected: 0x{expected:x})")
                return False
        
        return True
        
    except ImportError:
        print("⚠️  IntervalLib not yet available - need to move code first")
        return False
    except Exception as e:
        print(f"✗ Error testing IntervalLib: {e}")
        return False

def test_interval_class():
    """Test basic Interval functionality"""
    try:
        from memlayout import Interval
        
        # Create an interval
        interval = Interval(start=0x1000, size=0x2000, metadata={"type": "test"})
        print("✓ Created Interval instance")
        
        # Test basic properties
        if interval.start == 0x1000:
            print("✓ Correct start address")
        else:
            print(f"✗ Wrong start address: {interval.start}")
            return False
            
        if interval.size == 0x2000:
            print("✓ Correct size")
        else:
            print(f"✗ Wrong size: {interval.size}")
            return False
            
        if interval.end == 0x3000:
            print("✓ Correct end address")
        else:
            print(f"✗ Wrong end address: {interval.end}")
            return False
            
        # Test contains method
        if interval.contains(0x1500, 0x1000):
            print("✓ Contains method works")
        else:
            print("✗ Contains method failed")
            return False
            
        return True
        
    except ImportError:
        print("⚠️  Interval class not yet available - need to move code first")
        return False
    except Exception as e:
        print(f"✗ Error testing Interval: {e}")
        return False

def main():
    """Run all tests"""
    print("Running memlayout basic tests...")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_import():
        all_passed = False
    
    print()
    
    # Test Interval class
    if not test_interval_class():
        all_passed = False
        
    print()
    
    # Test IntervalLib
    if not test_interval_lib():
        all_passed = False
    
    print()
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed - check output above")
        
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)