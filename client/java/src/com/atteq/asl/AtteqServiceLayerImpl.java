package com.atteq.asl;

import org.apache.commons.httpclient.Header;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpMethod;
import org.apache.commons.httpclient.URI;
import org.apache.commons.httpclient.methods.EntityEnclosingMethod;
import org.apache.commons.httpclient.methods.StringRequestEntity;
import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.results.Result;
import com.atteq.asl.results.ResultTransformer;

public class AtteqServiceLayerImpl implements AtteqServiceLayer {

	private String serviceLayerUrl;
	private String securityToken;
	private boolean checkAslVersion = false;

	private final static String ASL_VERSION = "1.1";

	@Override
	public <T, R extends Result<T>> R perform(Performer performer, ResultTransformer<T, R> resultTransformer, JavaType t)
			throws ServiceCallException {
		try {
			HttpClient httpClient = new HttpClient();
			HttpMethod method = performer.getHttpMethod();
			method.setURI(new URI(String.format("%s/%s", serviceLayerUrl, performer.getUrl()), false));
			if (method instanceof EntityEnclosingMethod) {
				((EntityEnclosingMethod) method).setRequestEntity(new StringRequestEntity(performer.getBody(),
						performer.getContentType(), performer.getEncoding()));
			}
			httpClient.executeMethod(method);

			if (getCheckAslVersion()) {
				Header h = method.getResponseHeader("ASL-Flask-Layer");
				String serverVersion = (h == null ? "" : h.getValue());
				if (!serverVersion.startsWith(ASL_VERSION)) {
					throw new ServiceCallException(String.format(
							"The service version '%s' is not compatibile with the client version '%s'.", serverVersion,
							ASL_VERSION));
				}
			}

			return resultTransformer.transform(performer, method.getResponseBodyAsString(), method.getStatusCode(), t);
		} catch (Exception e) {
			throw new ServiceCallException(String.format("Error when calling ASL. %s", e.getMessage()), e);
		}
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

}
