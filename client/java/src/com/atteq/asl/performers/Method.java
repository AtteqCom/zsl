package com.atteq.asl.performers;

import com.atteq.asl.HttpMethod;
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
		return params.length > 0 ? 
			DEFAULT_METHOD_PREFIX + "/" + getName() + "/" + StringHelper.join("/", params) : 
			DEFAULT_METHOD_PREFIX + "/" + getName();
	}

	@Override
	public HttpMethod getHttpMethod() {
		return HttpMethod.POST;
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
