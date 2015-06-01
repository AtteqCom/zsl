package com.atteq.asl.performers;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.log4j.Logger;

import com.atteq.asl.HttpMethod;
import com.atteq.asl.ServiceCallException;
import com.atteq.asl.utils.JsonHelper;
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

		CREATE(HttpMethod.POST), READ(HttpMethod.GET), UPDATE(HttpMethod.PUT), DELETE(HttpMethod.DELETE);

		private final HttpMethod method;

		RequestType(HttpMethod method) {
			this.method = method;
		}

		public HttpMethod getMethod() {
			return this.method;
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
	public String getUrl() throws UnsupportedEncodingException {
		StringBuilder sb = new StringBuilder(StringHelper.join("/", DEFAULT_RESOURCE_PREFIX, getName(),
				StringHelper.join("/", StringHelper.encodeParams(getEncoding(), params))));

		if (args.size() > 0) {
			sb.append('?');
			for (Entry<String, String> e : args.entrySet()) {
				sb.append(String.format("%s=%s", URLEncoder.encode(e.getKey(), getEncoding()), URLEncoder.encode(e.getValue(), getEncoding())));
			}
		}

		return sb.toString();
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

			return JsonHelper.createMapper().writeValueAsString(data);
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
