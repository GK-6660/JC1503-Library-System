import pexpect
import sys
import os

def test_interactive_flow():
    # Delete the data file if it exists to start fresh
    data_file = "data/library_data.json"
    if os.path.exists(data_file):
        os.remove(data_file)
        
    print("Starting interactive test...")
    child = pexpect.spawn('python3 src/main.py', encoding='utf-8')
    child.logfile = sys.stdout
    
    # Wait for the initial data generation and the main menu
    child.expect('Enter choice:')
    
    # 1. Add User
    child.sendline('1')
    child.expect('ID:')
    child.sendline('TEST_U1')
    child.expect('Name:')
    child.sendline('Test User One')
    child.expect('User added ok!')
    
    # 2. Add Book
    child.expect('Enter choice:')
    child.sendline('2')
    child.expect('1. Book  2. Mag:')
    child.sendline('1')
    child.expect('ID:')
    child.sendline('TEST_B1')
    child.expect('Title:')
    child.sendline('Test Book Title')
    child.expect('Total:')
    child.sendline('1')
    child.expect('Author:')
    child.sendline('Test Author')
    child.expect('ISBN:')
    child.sendline('Test ISBN')
    child.expect('Item added successfully!')
    
    # 3. Borrow Book
    child.expect('Enter choice:')
    child.sendline('3')
    child.expect('User ID:')
    child.sendline('TEST_U1')
    child.expect('Title:')
    child.sendline('Test Book Title')
    child.expect('Borrow operation successful!')
    
    # 4. Show History
    child.expect('Enter choice:')
    child.sendline('6')
    child.expect('Type: borrow')
    
    # 5. Return Book
    child.expect('Enter choice:')
    child.sendline('4')
    child.expect('User ID:')
    child.sendline('TEST_U1')
    child.expect('Title:')
    child.sendline('Test Book Title')
    child.expect('Item returned successfully!')
    
    # 6. Exit
    child.expect('Enter choice:')
    child.sendline('0')
    child.expect('Data saved. Goodbye!')
    
    print("\n\nInteractive test completed successfully!")

if __name__ == '__main__':
    try:
        test_interactive_flow()
    except Exception as e:
        print(f"\n\nTest failed: {e}")
        sys.exit(1)