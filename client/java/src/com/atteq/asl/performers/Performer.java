package com.atteq.asl.performers;

import java.io.UnsupportedEncodingException;

import com.atteq.asl.HttpMethod;
import com.atteq.asl.ServiceCallException;

public interface Performer {

	public String getUrl() throws UnsupportedEncodingException;

	public HttpMethod getHttpMethod();

	public String getBody() throws ServiceCallException;

	public String getContentType();

	public String getEncoding();

}