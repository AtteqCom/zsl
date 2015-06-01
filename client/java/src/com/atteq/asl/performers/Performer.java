package com.atteq.asl.performers;

import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;

import com.atteq.asl.HttpMethod;
import com.atteq.asl.ServiceCallException;

public interface Performer {

	public URL getUrl(String scheme, String hostname) throws UnsupportedEncodingException, MalformedURLException, URISyntaxException;

	public HttpMethod getHttpMethod();

	public String getBody() throws ServiceCallException;

	public String getContentType();

	public String getEncoding();

}