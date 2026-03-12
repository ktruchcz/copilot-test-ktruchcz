package com.example;

/**
 * A simple Hello World application.
 */
public class HelloWorld {

    /**
     * Returns the greeting message.
     *
     * @return the greeting string
     */
    public String getGreeting() {
        return "Hello World";
    }

    /**
     * Application entry point.
     *
     * @param args command-line arguments (not used)
     */
    public static void main(String[] args) {
        HelloWorld app = new HelloWorld();
        System.out.println(app.getGreeting());
    }
}
