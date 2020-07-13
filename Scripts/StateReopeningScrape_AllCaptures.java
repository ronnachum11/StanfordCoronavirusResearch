import java.io.*;
import java.net.*;
import java.util.*;

public class StateReopeningScrape_AllCaptures {

	// alphabetical list of all fifty state names, as well as "District of Columbia"
	// NYTimes has reopening data for all fifty states, plus "District of Columbia";
	// later captures also have data for "Puerto Rico", but this is not collected
	static String[] states;
	// an array of URLs for the Internet Archive captures of the NYTimes state
	// reopening article, ordered chronologically
	static ArrayList<String> urls;
	// data.get([state name]).get([url]) = a String-to-String HashMap, where
	// keys are reopening categories ("Retail", "Personal Care"), and
	// values are the corresponding information ("Malls", "Hair salons and nail
	// salons")
	static HashMap<String, HashMap<String, HashMap<String, String>>> data;

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
		if (stringURL.equals("")) {
			for (String state : states) {
				data.get(state).put("", new HashMap<String, String>());
			}
			return;
		}
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
				if (line == null) {
					break;
				}
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
				continue;
			}
			data.get(state).put(stringURL, new HashMap<String, String>());
			// get categories and corresponding info
			// move to next state name upon reaching an undesired header (ex. "Reopening
			// Soon", "Closed"), or upon reaching the end of the current state's data
			while (true) {
				line = br.readLine();
				if (line == null) {
					break;
				}
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
						if (line == null) {
							break;
						}
						line = trimTo(line, "<");
						line = trimFrom(line, ">");
						if (line.length() >= lInfo.length() && line.substring(0, lInfo.length()).equals(lInfo)) {
							break;
						}
					}
					// note that info may be an empty string, especially if category = "Houses of
					// Worship"
					String info = line.substring(lInfo.length(), line.length() - endDiv.length());
					if (info.equals("")) {
						info = "[no info]";
					}
					// update data with category-info pair
					data.get(state).get(stringURL).put(category, info);
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
		data = new HashMap<String, HashMap<String, HashMap<String, String>>>();
		for (String state : states) {
			data.put(state, new HashMap<String, HashMap<String, String>>());
		}
		// initialize urls here
		urls = new ArrayList<String>();
		urls.add("");
		ArrayList<Integer> days = new ArrayList<Integer>();
		ArrayList<Integer> months = new ArrayList<Integer>();
		days.add(4);
		months.add(30);
		// start from 2020 May 1
		int month = 5;
		int day = 1;
		int[] daysInMonth = {0, 0, 0, 0, 0, 31, 30, 31, 31, 30, 31, 30, 31};
		// change endMonth and endDay as needed
		int endMonth = 7;
		int endDay = 10;
		while (endMonth != month || endDay != day) {
			String stringMonth = Integer.toString(month);
			if (month < 10) {
				stringMonth = "0" + stringMonth;
			}
			String stringDay = Integer.toString(day);
			if (day < 10) {
				stringDay = "0" + stringDay;
			}
			// note that Internet Archive uses 24-hour GMT
			// GMT is four hours ahead of New York's EST
			for (int hr : new int[]{16}) {
				String stringHr = Integer.toString(hr);
				if (hr < 10) {
					stringHr = "0" + stringHr;
				}
				urls.add("https://web.archive.org/web/2020"
						+ stringMonth
						+ stringDay
						+ stringHr
						+ "/https://www.nytimes.com/interactive/2020/us/states-reopen-map-coronavirus.html");
				days.add(day);
				months.add(month);
			}
			day++;
			if (day > daysInMonth[month]) {
				month++;
				day = 1;
			}
		}
		// get data
		int done = 0;
		for (String url : urls) {
			//System.out.println(url);
			extractData(url);
			done++;
			System.out.println(done + "/" + urls.size());
		}
		// use data to write output files (one for each state)
		System.out.println("Generating output...");
		for (String state : states) {
			BufferedWriter bw = new BufferedWriter(new FileWriter("Reopening of " + state + ".txt"));
			boolean writtenDate = false;
			for (int i = 1; i < urls.size(); i++) {
				if (days.get(i) != days.get(i - 1)) {
					writtenDate = false;
				}
				HashMap<String, String> curr = data.get(state).get(urls.get(i));
				HashMap<String, String> prev = data.get(state).get(urls.get(i - 1));
				// check for removed categories
				for (String category : prev.keySet()) {
					if (!curr.containsKey(category)) {
						if (!writtenDate) {
							bw.write(months.get(i) + "/" + days.get(i) + '\n');
							writtenDate = true;
						}
						bw.write("REMOVED" + '\n');
						bw.write(category + '\n');
						bw.write(prev.get(category) + '\n');
					}
				}
				// check for added categories
				for (String category : curr.keySet()) {
					if (!prev.containsKey(category)) {
						if (!writtenDate) {
							bw.write(months.get(i) + "/" + days.get(i) + '\n');
							writtenDate = true;
						}
						bw.write("ADDED" + '\n');
						bw.write(category + '\n');
						bw.write(curr.get(category) + '\n');
					}
				}
				// check for changed categories
				for (String category : curr.keySet()) {
					if (prev.containsKey(category) && !prev.get(category).equals(curr.get(category))) {
						if (!writtenDate) {
							bw.write(months.get(i) + "/" + days.get(i) + '\n');
							writtenDate = true;
						}
						bw.write("CHANGED" + '\n');
						bw.write(category + '\n');
						bw.write(prev.get(category) + '\n');
						bw.write(curr.get(category) + '\n');
					}
				}
			}
			bw.flush();
			bw.close();
		}
		System.out.println("Done!");
	}
}
