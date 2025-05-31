class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_node(self, data):#Add a node to the end of the list
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current=self.head
            while current.next is not None:
                current=current.next
            current.next=new_node
        self.size+=1
        return data  # Return the added data for batch confirmation

    def print_list(self):#Print all elements in the list
        current = self.head
        elements = []
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        print("Linked List: " + (" ".join(elements) if elements else "Empty"))

    def delete_nth_node(self, n):
        try:
            if self.head is None:
                raise ValueError("Cannot delete from an empty list")
                
            if n<1 or n>self.size:
                raise ValueError(f"Position must be between 1 and {self.size}")
                
            if n==1:
                deleted_data=self.head.data
                self.head=self.head.next
            else:
                current=self.head
                for _ in range(n-2):
                    current=current.next
                deleted_data=current.next.data
                current.next=current.next.next
                
            self.size-=1
            print(f"Deleted node at position {n} (value: {deleted_data})")
            return True
        except ValueError as e:
            print(f"ERROR!\nError: {e}")
            return False


def display_menu():
    print("\nLinked List Operations:")
    print("1. Add node(s) to end")
    print("2. Delete node by position")
    print("3. Print list")
    print("4. Exit")


def add_nodes_interactively(ll):#Handle adding multiple nodes with one command
    while True:
        try:
            count=int(input("How many nodes do you want to add? (0 to cancel): "))
            if count==0:
                return
            if count<0:
                print("Please enter a positive number.")
                continue
                added = []
            for i in range(1, count+1):
                data = input(f"Enter data for node {i}/{count}: ")
                added.append(ll.add_node(data))
                
            print(f"Added {len(added)} nodes: {', '.join(map(str, added))}")
            break
            
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    ll =LinkedList()
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        
        if choice=='1':
            add_nodes_interactively(ll)
        elif choice=='2':
            if ll.size==0:
                print("List is empty - nothing to delete")
                continue
            ll.print_list()
            try:
                position = int(input(f"Enter position to delete (1-{ll.size}): "))
                ll.delete_nth_node(position)
            except ValueError:
                print("ERROR!\nInvalid input. Please enter a valid number.")
        elif choice == '3':
            ll.print_list()
        elif choice == '4':
            print("Exiting program. Final list:")
            ll.print_list()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
if __name__ == "__main__":
    print("Week 2- Implement a Linked List in Python Using OOP and Delete the Nth Node")
    main()