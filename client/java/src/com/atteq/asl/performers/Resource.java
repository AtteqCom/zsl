package com.atteq.asl.performers;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.commons.httpclient.HttpMethod;
import org.apache.commons.httpclient.URIException;
import org.apache.commons.httpclient.methods.DeleteMethod;
import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.PutMethod;
import org.apache.commons.httpclient.util.URIUtil;
import org.apache.log4j.Logger;
import org.codehaus.jackson.map.ObjectMapper;

import com.atteq.asl.ServiceCallException;
import com.atteq.asl.utils.StringHelper;

public class Resource implements Performer {

	static final Logger logger = Logger.getLogger(Resource.class);

	private final String name;

	private final Map<String, String> args;

	private final Object data;

	private final String[] params;

	private final static String DEFAULT_RESOURCE_PREFIX = "resource";

	private final RequestType requestType;

	public static enum RequestType {

		CREATE(new PostMethod()), READ(new GetMethod()), UPDATE(new PutMethod()), DELETE(new DeleteMethod());

		private final HttpMethod method;

		RequestType(HttpMethod method) {
			this.method = method;
		}

		public HttpMethod getMethod() {
			return method;
		}

	}

	public Resource(String name, RequestType requestType, Object data, Map<String, String> args, String... params) {
		this.name = name;
		this.requestType = requestType;
		this.params = params;
		this.data = data;
		this.args = args == null ? new HashMap<String, String>() : args;
	}

	public String getName() {
		return name;
	}

	@Override
	public String getUrl() {
		StringBuilder query = new StringBuilder();
		for (Entry<String, String> e : args.entrySet()) {
			try {
				query.append(String.format("%s=%s",
						URIUtil.encodeWithinQuery(e.getKey(), URIUtil.encodeWithinQuery(e.getValue()))));
			} catch (URIException ex) {
				logger.error(ex);
			}
		}
		return DEFAULT_RESOURCE_PREFIX + "/" + getName() + StringHelper.joinParameters(params) + "?" + query;
	}

	@Override
	public HttpMethod getHttpMethod() {
		return requestType.getMethod();
	}

	@Override
	public String getBody() throws ServiceCallException {
		try {
			if (data == null) {
				return "";
			}

			return (new ObjectMapper()).writeValueAsString(data);
		} catch (Exception e) {
			throw new ServiceCallException("Error converting body to JSON when calling resource.", e);
		}
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
