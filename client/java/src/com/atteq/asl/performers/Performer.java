package com.atteq.asl.performers;

import com.atteq.asl.HttpMethod;
import com.atteq.asl.ServiceCallException;

public interface Performer {

	public String getUrl();

	public HttpMethod getHttpMethod();

	public String getBody() throws ServiceCallException;

	public String getContentType();

	public String getEncoding();

}