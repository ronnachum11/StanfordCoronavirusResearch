import java.io.*;
import java.net.*;
import java.util.*;

public class StateReopeningScrape_SingleCapture {

	// alphabetical list of all fifty state names, as well as "District of Columbia"
	// NYTimes has reopening data for all fifty states, plus "District of Columbia";
	// later captures also have data for "Puerto Rico", but this is not collected
	static String[] states;
	// data.get([state name]) = a String-to-String HashMap, where
	// keys are reopening categories ("Retail", "Personal Care"), and
	// values are the corresponding information ("Malls", "Hair salons and nail
	// salons")
	static HashMap<String, HashMap<String, String>> data;

	// returns BufferedReader that parses HTML from the given URL
	static BufferedReader getHTML(String stringURL) throws Exception {
		URL url = new URL(stringURL);
		URLConnection con = url.openConnection();
		InputStream is = con.getInputStream();
		BufferedReader br = new BufferedReader(new InputStreamReader(is));
		return br;
	}

	// returns a suffix of s, starting from the first instance of s1
	static String trimTo(String s, String s1) {
		if (!s.contains(s1)) {
			return "";
		}
		return s.substring(s.indexOf(s1));
	}

	// returns a prefix of s, ending at the last instance of s1
	static String trimFrom(String s, String s1) {
		if (!s.contains(s1)) {
			return "";
		}
		return s.substring(0, s.lastIndexOf(s1) + s1.length());
	}

	// extracts data from the content of the given URL
	static void extractData(String stringURL) throws Exception {
		BufferedReader br = getHTML(stringURL);
		// "landmark" strings come just before desired strings
		// the "\" character comes before inner double quotation marks
		String lState = "<div class=\"g-name\">";
		String lCategory = "<div class=\"g-cat-name\">";
		String lInfo = "<div class=\"g-cat-text\">";
		String lHeader = "<div class=\"g-details-subhed\">";
		String lWrap = "<div class=\"g-name-details-wrap\">";
		String endDiv = "</div>";
		// extract data for each state
		for (int i = 0; i < states.length; i++) {
			String line = "";
			// fast-foward to next state name
			while (true) {
				line = br.readLine();
				line = trimTo(line, "<");
				line = trimFrom(line, ">");
				if (line.length() >= lState.length() && line.substring(0, lState.length()).equals(lState)) {
					break;
				}
			}
			String state = line.substring(lState.length(), line.length() - endDiv.length());
			// check if current state is not in states (ex. state = "Puerto Rico")
			boolean inStates = false;
			for (int j = 0; j < states.length; j++) {
				if (state.equals(states[j])) {
					inStates = true;
				}
			}
			if (!inStates) {
				i--;
				// debug
				System.out.println();
				System.out.println("not collected: " + state);
				continue;
			}
			// debug
			System.out.println();
			System.out.println(state);
			// get categories and corresponding info
			// move to next state name upon reaching an undesired header (ex. "Reopening
			// Soon", "Closed"), or upon reaching the end of the current state's data
			while (true) {
				line = br.readLine();
				line = trimTo(line, "<");
				line = trimFrom(line, ">");
				// reaching header
				if (line.length() >= lHeader.length() && line.substring(0, lHeader.length()).equals(lHeader)) {
					String header = line.substring(lHeader.length(), line.length() - endDiv.length());
					if (!header.equals("Reopened") && !header.equals("Open")) {
						break;
					}
				}
				// reaching end of current state's data
				else if (line.length() >= lWrap.length() && line.substring(0, lWrap.length()).equals(lWrap)) {
					break;
				}
				// reaching next category
				else if (line.length() >= lCategory.length()
						&& line.substring(0, lCategory.length()).equals(lCategory)) {
					String category = line.substring(lCategory.length(), line.length() - endDiv.length());
					// get corresponding info
					while (true) {
						line = br.readLine();
						line = trimTo(line, "<");
						line = trimFrom(line, ">");
						if (line.length() >= lInfo.length() && line.substring(0, lInfo.length()).equals(lInfo)) {
							break;
						}
					}
					// note that info may be an empty string, especially if category = "Houses of
					// Worship"
					String info = line.substring(lInfo.length(), line.length() - endDiv.length());
					// debug
					System.out.println(category + ": " + info);
					// update data with category-info pair
					data.get(state).put(category, info);
				}
			}
		}
	}

	public static void main(String[] args) throws Exception {
		states = new String[] { "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
				"Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
				"Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
				"Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
				"New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
				"Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
				"Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming" };
		data = new HashMap<String, HashMap<String, String>>();
		for (String state : states) {
			data.put(state, new HashMap<String, String>());
		}
		// sample usage of extractData() with a 2020 June 30 08:38:51 capture
		extractData(
				"https://web.archive.org/web/20200630083851/https://www.nytimes.com/interactive/2020/us/states-reopen-map-coronavirus.html");
		// debug
		for (String state : states) {
			System.out.println(data.get(state));
		}
	}
}
