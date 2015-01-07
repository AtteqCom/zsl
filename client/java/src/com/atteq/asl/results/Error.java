package com.atteq.asl.results;

public class Error {

	String code;
	String message;

	Error() {
	}

	public Error(String code, String message) {
		super();
		this.code = code;
		this.message = message;
	}

	public String getCode() {
		return code;
	}

	public void setCode(String code) {
		this.code = code;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	public String toString() {
		return String.format("{code=%s, message=%s}", code, message);
	}

}
