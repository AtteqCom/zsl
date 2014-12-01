package com.atteq.asl;

public class ServiceCallException extends Exception {

	private static final long serialVersionUID = 1L;

	public ServiceCallException(String message) {
		super(message);
	}

	public ServiceCallException(String message, Exception e) {
		super(message, e);
	}

}
