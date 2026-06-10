#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// ----------- STRUCTURES -----------
struct Food {
    int id;
    char name[50];
    float price;
    struct Food *next;
};

struct Order {
    char name[50];
    int qty;
    float total;
    struct Order *next;
};

struct Food *menuHead = NULL;
struct Order *orderHead = NULL;
int idCounter = 1;

// ----------- INTEGER VALIDATION -----------
int getInt() {
    int value;
    char ch;

    while (1) {
        if (scanf("%d", &value) == 1)
            return value;
        else {
            printf("❌ Enter numbers only: ");
            while ((ch = getchar()) != '\n' && ch != EOF);
        }
    }
}

// ----------- STRING VALIDATION -----------
int isValidName(char str[]) {
    for (int i = 0; str[i] != '\0'; i++) {
        if (!(isalnum(str[i]) || str[i] == ' '))
            return 0;
    }
    return 1;
}

void getString(char str[], int size) {
    char ch;

    while (1) {
        fgets(str, size, stdin);
        str[strcspn(str, "\n")] = 0;

        if (isValidName(str))
            return;
        else
            printf("❌ Use only letters, numbers, spaces: ");

        while ((ch = getchar()) != '\n' && ch != EOF);
    }
}

// ----------- ADMIN LOGIN -----------
int adminLogin() {
    char user[20], pass[20];

    printf("\n--- ADMIN LOGIN ---\n");
    printf("Username: ");
    scanf("%s", user);
    printf("Password: ");
    scanf("%s", pass);

    return (strcmp(user, "admin") == 0 && strcmp(pass, "1234") == 0);
}

// ----------- ADD FOOD -----------
void addFood() {
    struct Food newNode = (struct Food)malloc(sizeof(struct Food));

    newNode->id = idCounter++;

    printf("Enter food name: ");
    getchar();
    getString(newNode->name, 50);

    printf("Enter price: ");
    scanf("%f", &newNode->price);

    newNode->next = NULL;

    if (menuHead == NULL)
        menuHead = newNode;
    else {
        struct Food *temp = menuHead;
        while (temp->next != NULL)
            temp = temp->next;
        temp->next = newNode;
    }

    printf("✅ Food added!\n");
}

// ----------- DISPLAY MENU -----------
void displayMenu() {
    if (menuHead == NULL) {
        printf("Menu is empty!\n");
        return;
    }

    struct Food *temp = menuHead;
    printf("\n--- MENU ---\n");

    while (temp != NULL) {
        printf("ID:%d | %s | ₹%.2f\n",
               temp->id, temp->name, temp->price);
        temp = temp->next;
    }
}

// ----------- SEARCH FOOD -----------
struct Food* searchFood(char name[]) {
    struct Food *temp = menuHead;

    while (temp != NULL) {
        if (strcasecmp(temp->name, name) == 0)
            return temp;
        temp = temp->next;
    }
    return NULL;
}

// ----------- DELETE FOOD -----------
void deleteFood() {
    int id;
    printf("Enter ID to delete: ");
    id = getInt();

    struct Food *temp = menuHead, *prev = NULL;

    if (temp != NULL && temp->id == id) {
        menuHead = temp->next;
        free(temp);
        printf("Deleted!\n");
        return;
    }

    while (temp != NULL && temp->id != id) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("Food not found!\n");
        return;
    }

    prev->next = temp->next;
    free(temp);
    printf("Deleted!\n");
}

// ----------- PLACE ORDER -----------
void placeOrder() {
    char name[50];
    int qty;

    displayMenu();

    printf("\nEnter food name: ");
    getchar();
    getString(name, 50);

    struct Food *food = searchFood(name);

    if (food == NULL) {
        printf("❌ Not Available!\n");
        return;
    }

    printf("Enter quantity: ");
    qty = getInt();

    struct Order newOrder = (struct Order)malloc(sizeof(struct Order));

    strcpy(newOrder->name, food->name);
    newOrder->qty = qty;
    newOrder->total = qty * food->price;
    newOrder->next = NULL;

    if (orderHead == NULL)
        orderHead = newOrder;
    else {
        struct Order *temp = orderHead;
        while (temp->next != NULL)
            temp = temp->next;
        temp->next = newOrder;
    }

    printf("✅ Order placed!\n");
}

// ----------- BILL -----------
void generateBill() {
    if (orderHead == NULL) {
        printf("No orders!\n");
        return;
    }

    struct Order *temp = orderHead;
    float total = 0;

    printf("\n===== BILL =====\n");

    while (temp != NULL) {
        printf("%s x%d = ₹%.2f\n",
               temp->name, temp->qty, temp->total);
        total += temp->total;
        temp = temp->next;
    }

    printf("-------------------\n");
    printf("Total = ₹%.2f\n", total);
}

// ----------- ADMIN PANEL -----------
void adminPanel() {
    int ch;

    while (1) {
        printf("\n--- ADMIN ---\n");
        printf("1. Add Food\n2. Delete Food\n3. View Menu\n4. Logout\nChoice: ");
        ch = getInt();

        switch (ch) {
            case 1: addFood(); break;
            case 2: deleteFood(); break;
            case 3: displayMenu(); break;
            case 4: return;
            default: printf("Invalid!\n");
        }
    }
}

// ----------- USER PANEL -----------
void userPanel() {
    int ch;

    while (1) {
        printf("\n--- USER ---\n");
        printf("1. View Menu\n2. Order Food\n3. Bill\n4. Back\nChoice: ");
        ch = getInt();

        switch (ch) {
            case 1: displayMenu(); break;
            case 2: placeOrder(); break;
            case 3: generateBill(); break;
            case 4: return;
            default: printf("Invalid!\n");
        }
    }
}

// ----------- MAIN -----------
int main() {
    int choice;

    while (1) {
        printf("\n===== RESTAURANT SYSTEM =====\n");
        printf("1. Admin\n2. Consumer\n3. Exit\nChoice: ");
        choice = getInt();

        switch (choice) {
            case 1:
                if (adminLogin())
                    adminPanel();
                else
                    printf("❌ Wrong login!\n");
                break;

            case 2:
                userPanel();
                break;

            case 3:
                exit(0);

            default:
                printf("Invalid!\n");
        }
    }
}
