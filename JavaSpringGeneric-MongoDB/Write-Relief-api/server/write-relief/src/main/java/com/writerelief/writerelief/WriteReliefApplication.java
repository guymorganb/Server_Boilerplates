package com.writerelief.writerelief;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * @SpringBootApplication is a convenience annotation that adds all of the
 *                        following:
 * 
 * @Configuration: Tags the class as a source of bean definitions for the
 *                 application context.
 * @EnableAutoConfiguration: Tells Spring Boot to start adding beans based on
 *                           classpath settings, other beans, and various
 *                           property settings.
 * @ComponentScan: Tells Spring to look for other components, configurations,
 *                 and services in the com.writerelief package, allowing it to
 *                 find controllers, services, and other components.
 */
@SpringBootApplication
public class WriteReliefApplication {

	public static void main(String[] args) {
		SpringApplication.run(WriteReliefApplication.class, args);

		System.out.println("Hello World");
	}

}
