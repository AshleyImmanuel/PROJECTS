#include <stdio.h>
#include <stdlib.h>
#include<conio.h>
typedef struct node {
    int data;
    struct node* next;
    struct node* prev;
} node;

node* head = NULL;  // Global head
void insert() {
    int value;
    printf("Enter value: ");
    scanf("%d", &value);
    node* new = (node*)malloc(sizeof(node));
    new->data = value;
    new->next = NULL;
    new->prev = NULL;
    if (head == NULL) {
        head = new;  // First node becomes head
    } else {
        node* temp = head;
        while (temp->next != NULL) {  
            temp = temp->next;  // Move to the last node
        }
        temp->next = new;  
        new->prev = temp;  
    }
}

void delete() {
    if (head == NULL) {
        printf("List is empty!\n");
        return;
    }

    int value;
    printf("Enter value to delete: ");
    scanf("%d", &value);

    node* temp = head;

    while (temp != NULL && temp->data != value) {
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("Not found!\n");
        return;
    }

    if (temp->prev == NULL && temp->next == NULL) {
        head = NULL;  // Only one node so list becomes empty
    } else if (temp->prev == NULL) {
        head = temp->next;  // Deleting first node
        head->prev = NULL;
    } else if (temp->next == NULL) {
        temp->prev->next = NULL;  // Deleting last node
    } else {
        temp->prev->next = temp->next;  // Deleting middle node
        temp->next->prev = temp->prev;
    }

    free(temp);
    printf("Deleted successfully!\n");
}

void search() {
    if (head == NULL) {
        printf("List is empty!\n");
        return;
    }

    int value, pos = 1;
    printf("Enter value to search: ");
    scanf("%d", &value);

    node* temp = head;

    while (temp != NULL) {
        if (temp->data == value) {
            printf("Found at position %d\n", pos);
            return;
        }
        temp = temp->next;
        pos++;
    }

    printf("Not found!\n");
}

void display() {
    if (head == NULL) {
        printf("List is empty!\n");
        return;
    }

    node* temp = head;
    printf("DLL: ");
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

int main() {
    int choice;
    clrscr();
    while (1) {
        printf("\n1. Insert\n2. Delete\n3. Search\n4. Display\n5. Exit\nEnter choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1: insert(); break;
            case 2: delete(); break;
            case 3: search(); break;
            case 4: display(); break;
            case 5: return 0;
            default: printf("Invalid choice!\n");
        }
    }
}

