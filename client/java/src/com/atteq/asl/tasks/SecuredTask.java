package com.atteq.asl.tasks;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import org.apache.commons.codec.binary.Hex;

import com.atteq.asl.SecuredAtteqServiceLayer;
import com.atteq.asl.ServiceCallException;
import com.atteq.asl.utils.StringHelper;
import com.fasterxml.jackson.annotation.JsonProperty;

public class SecuredTask extends Task {

	static class SecurityInfo {

		final String randomToken;

		final String hashedToken;

		public SecurityInfo(String secureToken) throws NoSuchAlgorithmException {
			this.randomToken = StringHelper.getRandomString(32);
			this.hashedToken = sha1(randomToken + secureToken);
		}

		private static String sha1(String data) throws NoSuchAlgorithmException {
			MessageDigest digest = MessageDigest.getInstance("SHA-1");
			byte[] digestResult = digest.digest(data.getBytes());
			return Hex.encodeHexString(digestResult).toUpperCase();
		}

		@JsonProperty("random_token")
		public String getRandomToken() {
			return randomToken;
		}

		@JsonProperty("hashed_token")
		public String getHashedToken() {
			return hashedToken;
		}

	}

	private SecurityInfo securityInfo;

	public SecuredTask(String name, Object data, SecuredAtteqServiceLayer asl) throws NoSuchAlgorithmException {
		super(name, data);
		this.securityInfo = new SecurityInfo(asl.getSecurityToken());
	}
	
	private static class Data {
		
		public Data(SecurityInfo info, Object data) {
			this.security = info;
			this.data = data;
		}
		
		
		// Used in JSON mapping.
		@SuppressWarnings("unused")
		public Object data;
		
		// Used in JSON mapping.
		@SuppressWarnings("unused")
		public SecurityInfo security;
		
	}

	@Override
	public Object getData() throws ServiceCallException {
		return new Data(securityInfo, super.getData());
	}

}
