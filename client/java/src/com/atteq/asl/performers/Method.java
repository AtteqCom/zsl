package com.atteq.asl.performers;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;

import com.atteq.asl.HttpMethod;
import com.atteq.asl.ServiceCallException;
import com.atteq.asl.utils.StringHelper;

public class Method implements Performer {

	private final String name;

	private final String[] params;

	private final static String DEFAULT_METHOD_PREFIX = "/method";

	public Method(String name, String... params) {
		this.name = name;
		this.params = params;
	}

	public String getName() {
		return name;
	}

	@Override
	public URL getUrl(String scheme, String hostname) throws MalformedURLException, URISyntaxException {
		return (params.length > 0 ?
				new URI(scheme, null, hostname, -1, StringHelper.join("/", DEFAULT_METHOD_PREFIX, getName(), StringHelper.join("/",  params)), null, null) :
				new URI(scheme, null, hostname, -1, DEFAULT_METHOD_PREFIX + "/" + getName(), null, null)).toURL();
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
		return "UTF`-8";
	}

}
