package com.atteq.asl.performers;

import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.utils.URIBuilder;
import org.apache.log4j.Logger;

import com.atteq.asl.ServiceCallException;
import com.atteq.asl.utils.JsonHelper;

public class Resource implements Performer {

	static final Logger logger = Logger.getLogger(Resource.class);

	private final String name;

	private final Map<String, String> args;

	private final Object data;

	private final String[] params;

	private final static String DEFAULT_RESOURCE_PREFIX = "resource";

	private final RequestType requestType;

	public static enum RequestType {

		CREATE(HttpPost.class), READ(HttpGet.class), UPDATE(HttpPut.class), DELETE(HttpDelete.class);

		private final Class<? extends HttpUriRequest> method;

		RequestType(Class<? extends HttpUriRequest> method) {
			this.method = method;
		}

		public HttpUriRequest getMethod() {
			try {
				return this.method.newInstance();
			} catch (Exception e) {
				logger.error(e);
				return null;
			}
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
		try {
			URIBuilder b = new URIBuilder(DEFAULT_RESOURCE_PREFIX + "/" + getName() + "/" + String.join("/", params));

			for (Entry<String, String> e : args.entrySet()) {
				b.addParameter(e.getKey(), e.getValue());
			}

			return b.build().toString();
		} catch (URISyntaxException e) {
			logger.error(e);
			return null;
		}
	}

	@Override
	public HttpUriRequest getHttpMethod() {
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
