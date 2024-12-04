// Example using tryagain

counter = 0;

try:
    counter = counter + 1;
    if (counter < 3) {
        // Simulating an error using a function call
        error();
    }
    show("Operation succeeded on attempt " + counter);
catch:
    show(counter);
    show("Error detected. Trying again...");
    tryagain();
