package com.atteq.asl.utils;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.text.Normalizer;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.regex.Pattern;

/**
 * String helper.
 */
public abstract class StringHelper {

	private static final String SAFE_PATTERN = "[^-a-zA-Z_0-9]+";
	private static final String REMOVE_ACCENT_PATTERN = "\\p{InCombiningDiacriticalMarks}+";
	private static final String RANDOM_PATTERN = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	private static final String DOTS = "...";

	/**
	 * Check if string is null or empty.
	 *
	 * @param text
	 *            String.
	 * @return True on success or false if contains some characters.
	 */
	public static boolean isNullOrEmpty(final String text) {
		return text == null || text.isEmpty();
	}

	/**
	 * Check if string is null or empty or contains only whitespace.
	 *
	 * @param text
	 *            String.
	 * @return True on success or false if contains any non-whitespace
	 *         character.
	 */
	public static boolean isNullOrWhitespace(final String text) {
		return text == null || text.isEmpty() || text.trim().isEmpty();
	}

	/**
	 * Checks if the string is null or empty.
	 *
	 * @param string
	 *            String to be checked for emptiness.
	 * @return {@code True} if the string is empty or contains only white space.
	 */
	public static boolean isEmpty(final String string) {
		return string == null || string.trim().length() == 0;
	}

	/**
	 * Makes the first letter lower case.
	 *
	 * @param string
	 *            String that will have its first letter in lowercase form.
	 * @return First letter in lowercase.
	 */
	public static String firstToLower(final String string) {
		if (isEmpty(string)) {
			return string;
		} else {
			StringBuilder b = new StringBuilder(string);
			b.setCharAt(0, Character.toLowerCase(string.charAt(0)));
			return b.toString();
		}
	}

	/**
	 * Returns string containing only letters, numbers, '-' and '_'.
	 *
	 * @param s
	 *            String containing any character.
	 * @return String from which any other than mentioned characters are
	 *         removed.
	 */
	public static String getSafeString(String s) {
		String noAccent = removeAccent(s);
		noAccent = Pattern.compile("[ ]+").matcher(noAccent).replaceAll("-");
		noAccent = Pattern.compile(SAFE_PATTERN).matcher(noAccent).replaceAll("");
		return noAccent;
	}

	/**
	 * Removes accent from given string.
	 *
	 * @param s
	 *            String containing accent characters.
	 * @return String without accent characters.
	 */
	public static String removeAccent(String s) {
		String temp = Normalizer.normalize(s, Normalizer.Form.NFD);
		Pattern pattern = Pattern.compile(REMOVE_ACCENT_PATTERN);
		return pattern.matcher(temp).replaceAll("");
	}

	/**
	 * Truncates a String to the given length.
	 *
	 * @param value
	 *            String to be truncated
	 * @param length
	 *            Maximum length of string
	 * @return Returns value if value is null or value.length() is less or equal
	 *         to length, otherwise a String representing value truncated to
	 *         length with added dots (...)
	 */
	public static String truncate(String value, int length) {
		if (value != null && value.length() > length) {
			value = value.substring(0, length);
			value += DOTS;
		}
		return value;
	}

	/**
	 * Generate random string for password
	 *
	 * @param randomPasswordLength
	 *            Length
	 * @return Random string of specified length
	 */
	public static String getRandomString(int randomPasswordLength) {
		return getRandomString(randomPasswordLength, RANDOM_PATTERN);
	}

	/**
	 * Generate random string for password consisting of specified chars
	 *
	 * @param randomPasswordLength
	 *            Length
	 * @param characters
	 *            String defining characters to use
	 * @return Random string of specified length containing specified characters
	 *         only
	 */
	public static String getRandomString(int randomPasswordLength, String characters) {
		Random rng = new Random();

		char[] text = new char[randomPasswordLength];
		for (int i = 0; i < randomPasswordLength; ++i) {
			text[i] = characters.charAt(rng.nextInt(characters.length()));
		}
		return new String(text);
	}

	/**
	 * Check whenever string is valid unsigned number
	 *
	 * @param number
	 *            Number to check
	 * @return Whenever the string represents valid unsigned number
	 */
	public static boolean isValidUnsignedNumber(final String number) {
		try {
			Integer.parseInt(number);
			return true;
		} catch (NumberFormatException e) {
			return false;
		}
	}

	/**
	 * Joins the given {@code params} using delimiter.
	 * 
	 * @param delimiter
	 *            Delimiter.
	 * @param params
	 *            The parameters to be joined.
	 * @return The joined text.
	 */
	public static String join(String delimiter, String... params) {
		return join(delimiter, Arrays.asList(params));
	}

	/**
	 * Joins the given {@code params} using delimiter.
	 * 
	 * @param delimiter
	 *            Delimiter.
	 * @param params
	 *            The parameters to be joined.
	 * @return The joined text.
	 */
	public static String join(String delimiter, List<String> params) {
		if (params.size() == 0) {
			return "";
		} else if (params.size() == 1) {
			return params.get(0);
		} else {
			StringBuilder sb = new StringBuilder();
			sb.append(params.get(0));
			for (int i = 1; i < params.size(); ++i) {
				sb.append(delimiter);
				sb.append(params.get(i));
			}
			return sb.toString();
		}
	}

	/**
	 * Encodes the list of path parts that will be separated by /.
	 * 
	 * @param encoding
	 *            Encoding.
	 * @param params
	 *            Parameters to be encoded.
	 * @return The encoded array of parameters.
	 * @throws UnsupportedEncodingException
	 *             If the encoding is not supported.
	 */
	public static List<String> encodeParams(String encoding, String... params) throws UnsupportedEncodingException {
		List<String> encodedParams = Arrays.asList(params);

		for (int i = 0; i < encodedParams.size(); ++i) {
			encodedParams.set(i, URLEncoder.encode(params[i], encoding));
		}

		return encodedParams;
	}

}
