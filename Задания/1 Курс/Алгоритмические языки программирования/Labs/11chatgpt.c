#include <stdio.h>
#include <string.h>

#define MAX_BUSES 100 // Maximum number of buses

// Structure to represent time
struct Time {
    int hour;
    int minute;
};

// Structure to represent intercity bus
struct Bus {
    int number; // Bus number
    char from[50]; // Departure city
    char to[50]; // Destination city
    struct Time departure; // Departure time
    struct Time arrival; // Arrival time
};

// Function to get data about buses going to a specified city
void getBusesToCity(struct Bus buses[], int n, char city[]) {
    int i;

    printf("Buses going to %s:\n", city);

    for (i = 0; i < n; i++) {
        if (strcmp(buses[i].to, city) == 0) {
            printf("Bus #%d: from %s to %s, departure at %02d:%02d, arrival at %02d:%02d\n",
                   buses[i].number, buses[i].from, buses[i].to,
                   buses[i].departure.hour, buses[i].departure.minute,
                   buses[i].arrival.hour, buses[i].arrival.minute);
        }
    }
}

int main() {
    int i, n;
    char city[50];
    struct Bus buses[MAX_BUSES];

    // Fill in data about the buses
    printf("Enter the number of buses: ");
    scanf("%d", &n);

    for (i = 0; i < n; i++) {
        printf("Bus #%d:\n", i + 1);
        printf("  Number: ");
        scanf("%d", &buses[i].number);
        printf("  Departure city: ");
        scanf("%s", buses[i].from);
        printf("  Destination city: ");
        scanf("%s", buses[i].to);
        printf("  Departure time (hh:mm): ");
        scanf("%d:%d", &buses[i].departure.hour, &buses[i].departure.minute);
        printf("  Arrival time (hh:mm): ");
        scanf("%d:%d", &buses[i].arrival.hour, &buses[i].arrival.minute);
    }

    // Get data about buses going to a specified city
    printf("Enter the name of the city: ");
    scanf("%s", city);

    getBusesToCity(buses, n, city);

    return 0;
}