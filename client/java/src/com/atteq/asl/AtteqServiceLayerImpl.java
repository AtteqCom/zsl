package com.atteq.asl;

import java.io.BufferedOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;

import org.apache.log4j.Logger;
import org.codehaus.jackson.map.type.TypeFactory;
import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.results.GenericResult;
import com.atteq.asl.results.GenericResultFactory;
import com.atteq.asl.results.JsonResultTransformer;
import com.atteq.asl.results.Result;
import com.atteq.asl.results.ResultTransformer;
import com.atteq.asl.tasks.JsonResultWithErrorTransformer;
import com.atteq.asl.tasks.Task;
import com.atteq.asl.tasks.TaskResult;
import com.atteq.asl.tasks.TaskResultFactory;
import com.atteq.asl.utils.StringHelper;
import com.google.common.io.CharStreams;

public class AtteqServiceLayerImpl implements AtteqServiceLayer {

	private String serviceLayerUrl;
	private String securityToken;
	private boolean checkAslVersion = false;
	static Logger logger = Logger.getLogger(AtteqServiceLayerImpl.class);

	private final static String ASL_VERSION = "1.1";

	@Override
	public <T, R extends Result<T>> R perform(Performer performer, ResultTransformer<T, R> resultTransformer, JavaType t) throws ServiceCallException {
		try {
			URI baseUri = new URI(serviceLayerUrl);
			URL url = performer.getUrl(baseUri.getScheme(), baseUri.getHost());

			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod(performer.getHttpMethod().toString());

			String body = performer.getBody();
			logger.debug(String.format("%s %s", performer.getHttpMethod(), url));
			logger.debug(body);

			if ((performer.getHttpMethod() == HttpMethod.POST || performer.getHttpMethod() == HttpMethod.PUT) && !StringHelper.isNullOrEmpty(body)) {
				conn.setRequestProperty("Content-Type", performer.getContentType() + "; charset=" + performer.getEncoding());
				conn.setRequestProperty("Content-Length", Integer.toString(body.getBytes().length));
				conn.setDoOutput(true);
				OutputStreamWriter os = new OutputStreamWriter(new BufferedOutputStream(conn.getOutputStream()));
				os.write(body);
				os.close();
			}

			if (getCheckAslVersion()) {
				String h = conn.getHeaderField("ASL-Flask-Layer");
				String serverVersion = (h == null ? "" : h);
				if (!serverVersion.startsWith(ASL_VERSION)) {
					throw new ServiceCallException(String.format("The service version '%s' is not compatibile with the client version '%s'.", serverVersion,
							ASL_VERSION));
				}
			}

			String result = CharStreams.toString(new InputStreamReader(conn.getResponseCode() == HTTP_STATUS_CODE_OK ? conn.getInputStream() : conn
					.getErrorStream()));
			logger.debug(String.format("Response:\n%s", result));
			return resultTransformer.transform(performer, result, conn.getResponseCode(), t);
		} catch (Exception e) {
			throw new ServiceCallException(String.format("Error when calling ASL. %s", e.getMessage()), e);
		}
	}

	public <T, R extends Result<T>> R perform(Performer performer, ResultTransformer<T, R> resultTransformer, Class<T> c) throws ServiceCallException {
		return perform(performer, resultTransformer, TypeFactory.defaultInstance().constructType(c));
	}

	public <T> TaskResult<T> perform(Task task, JavaType t) throws ServiceCallException {
		TaskResultFactory<T> f = new TaskResultFactory<T>();
		return perform(task, new JsonResultTransformer<T, TaskResult<T>>(f), t);
	}

	public <T> TaskResult<T> perform(Task task, Class<T> c) throws ServiceCallException {
		TaskResultFactory<T> f = new TaskResultFactory<T>();
		return perform(task, new JsonResultTransformer<T, TaskResult<T>>(f), TypeFactory.defaultInstance().constructType(c));
	}

	public <T> TaskResult<T> performWithErrorDecorator(Task task, JavaType t) throws ServiceCallException {
		return perform(task, new JsonResultWithErrorTransformer<T>(), t);
	}

	public <T> TaskResult<T> performWithErrorDecorator(Task task, Class<T> c) throws ServiceCallException {
		return perform(task, new JsonResultWithErrorTransformer<T>(), TypeFactory.defaultInstance().constructType(c));
	}

	public <T> GenericResult<T> perform(Performer performer, JavaType t) throws ServiceCallException {
		GenericResultFactory<T> f = new GenericResultFactory<T>();
		return perform(performer, new JsonResultTransformer<T, GenericResult<T>>(f), t);
	}

	public <T> GenericResult<T> perform(Performer performer, Class<T> c) throws ServiceCallException {
		GenericResultFactory<T> f = new GenericResultFactory<T>();
		return perform(performer, new JsonResultTransformer<T, GenericResult<T>>(f), TypeFactory.defaultInstance().constructType(c));
	}

	public String getServiceLayerUrl() {
		return serviceLayerUrl;
	}

	public void setServiceLayerUrl(String serviceLayerUrl) {
		this.serviceLayerUrl = serviceLayerUrl;
	}

	public String getSecurityToken() {
		return securityToken;
	}

	public void setSecurityToken(String securityToken) {
		this.securityToken = securityToken;
	}

	public boolean getCheckAslVersion() {
		return checkAslVersion;
	}

	public void setCheckAslVersion(boolean checkAslVersion) {
		this.checkAslVersion = checkAslVersion;
	}

	public static final int HTTP_STATUS_CODE_OK = 200;

}
