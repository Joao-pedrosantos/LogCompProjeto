// Example using tryagain with attempt limit

counter = 0;
max_attempts = 3;

try:
    counter = counter + 1;
    press "Simulating action", 1;
    // Forcing an error
    undefined_variable;
    show("Operation succeeded on attempt " + counter);
catch:
    show("Error detected on attempt " + counter + ".");
    if (counter < max_attempts) {
        show("Trying again...");
        tryagain();
    } else {
        show("Maximum number of attempts reached.");
    }
