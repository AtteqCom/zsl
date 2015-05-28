package com.atteq.asl.performers;

import org.apache.http.client.methods.HttpUriRequest;

import com.atteq.asl.ServiceCallException;

public interface Performer {

	public String getUrl();

	public HttpUriRequest getHttpMethod();

	public String getBody() throws ServiceCallException;

	public String getContentType();

	public String getEncoding();

}