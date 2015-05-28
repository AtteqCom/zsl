package com.atteq.asl.tasks;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;

import com.atteq.asl.HttpMethod;
import com.atteq.asl.ServiceCallException;
import com.atteq.asl.performers.Performer;
import com.atteq.asl.utils.JsonHelper;

public class Task implements Performer {

	private static final String DEFAULT_CONTENT_TYPE = "application/json";

	private static final String DEFAULT_ENCODING = "utf-8";

	private final static String DEFAULT_TASK_PREFIX = "task";

	private String contentType;

	private String encoding;

	private final String name;

	private Object data;

	public Task(String name, Object data) {
		this(name, data, DEFAULT_CONTENT_TYPE, DEFAULT_ENCODING);
	}

	public Task(String name, Object data, String contentType) {
		this(name, data, contentType, DEFAULT_ENCODING);
	}

	public Task(String name, Object data, String contentType, String encoding) {
		this.name = name;
		this.data = data;
		this.contentType = contentType;
		this.encoding = encoding;
	}

	public String getName() {
		return name;
	}

	public Object getData() {
		return data;
	}

	public void setData(Object data) {
		this.data = data;
	}

	@Override
	public String getUrl() {
		return DEFAULT_TASK_PREFIX + "/" + getName();
	}

	@Override
	public HttpMethod getHttpMethod() {
		return HttpMethod.POST; 
	}

	@Override
	public String getBody() throws ServiceCallException {
		Object data = getData();
		if (data == null) {
			return null;
		}
		
		ByteArrayOutputStream ss = new ByteArrayOutputStream();
		ObjectMapper objectMapper = JsonHelper.createMapper();
		try {
			objectMapper.writeValue(ss, data);
		} catch (JsonGenerationException e) {
			throw new ServiceCallException("Could not generate JSON from the object data.", e);
		} catch (JsonMappingException e) {
			throw new ServiceCallException("Could not map JSON to the object data.", e);
		} catch (IOException e) {
			throw new ServiceCallException("IO error while converting to JSON.", e);
		}

		try {
			return ss.toString("UTF-8");
		} catch (UnsupportedEncodingException e) {
			throw new ServiceCallException("IO error while converting to JSON.", e);
		}
	}

	@Override
	public String getContentType() {
		return contentType;
	}

	@Override
	public String getEncoding() {
		return encoding;
	}
}
