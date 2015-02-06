package com.atteq.asl.performers;

import org.apache.commons.httpclient.HttpMethod;
import org.apache.commons.httpclient.methods.PostMethod;

import com.atteq.asl.ServiceCallException;
import com.atteq.asl.utils.StringHelper;

public class Method implements Performer {

	private final String name;

	private final String[] params;

	private final static String DEFAULT_METHOD_PREFIX = "method";

	public Method(String name, String... params) {
		this.name = name;
		this.params = params;
	}

	public String getName() {
		return name;
	}

	@Override
	public String getUrl() {
		return DEFAULT_METHOD_PREFIX + "/" + getName() + StringHelper.joinParameters(params);
	}

	@Override
	public HttpMethod getHttpMethod() {
		return new PostMethod();
	}

	@Override
	public String getBody() throws ServiceCallException {
		return "";
	}

	@Override
	public String getContentType() {
		return "application/json";
	}

	@Override
	public String getEncoding() {
		return "utf-8";
	}

}
