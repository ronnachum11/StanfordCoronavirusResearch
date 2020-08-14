import java.io.*;
import java.net.*;
import java.util.*;

public class StateReopening_WaPo_PlacesOfWorship {

	static String[] states;
	static ArrayList<String> urls;
	// dateOpened.get(state) = day that the state initially reopened places of worship (May 8 is given if actual date is earlier than May 8) 
	static HashMap<String, String> dateOpened;
	static ArrayList<String> keywords;
	static ArrayList<Integer> days, months;
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
	static void extractData(int index) throws Exception {
		BufferedReader br = getHTML(urls.get(index));
		// "landmark" strings come just before desired strings
		// the "\" character must be put in front of inner quotation marks
		String lState = "<h3 class=\"font--headline bold font-lg pb-xs\">";
		// extract data for each state
		for (int i = 0; i < states.length; i++) {
			String line = "";
			// fast-foward to next state name
			while (true) {
				line = br.readLine();
				if (line == null) {
					break;
				}
				if (line.contains(lState)) {
					int indexOfState = line.indexOf(lState) + lState.length();
					String state = line.substring(indexOfState, line.indexOf("<", indexOfState));
					// check if current state is not in states (ex. state = "Puerto Rico")
					boolean inStates = false;
					for (int j = 0; j < states.length; j++) {
						if (state.equals(states[j])) {
							inStates = true;
						}
					}
					if (!inStates) {
						// end while-loop and look for next state
						i--;
						break;
					}
					// check if state has reopened places of worship, update dateOpened if needed
					for (String keyword: keywords) {
						if (line.toLowerCase().contains(keyword) && !dateOpened.containsKey(state)) {
							dateOpened.put(state, months.get(index) + "/" + days.get(index));
						}
					}
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
		dateOpened = new HashMap<String, String>();
		// initialize keywords (lowercase characters only)
		keywords = new ArrayList<String>();
		keywords.add("church");
		keywords.add("worship");
		// initialize urls
		urls = new ArrayList<String>();
		days = new ArrayList<Integer>();
		months = new ArrayList<Integer>();
		// start from 2020 May 1
		int month = 5;
		int day = 8;
		int[] daysInMonth = {0, 0, 0, 0, 0, 31, 30, 31, 31, 30, 31, 30, 31};
		// change endMonth and endDay as needed
		int endMonth = 7;
		int endDay = 29;
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
			// gets one archive per day at 16:00 GMT, or 12:00 EST
			for (int hr : new int[]{16}) {
				String stringHr = Integer.toString(hr);
				if (hr < 10) {
					stringHr = "0" + stringHr;
				}
				urls.add("https://web.archive.org/web/2020"
						+ stringMonth
						+ stringDay
						+ stringHr
						+ "/https://www.washingtonpost.com/graphics/2020/national/states-reopening-coronavirus-map/");
				days.add(day);
				months.add(month);
			}
			day++;
			if (day > daysInMonth[month]) {
				month++;
				day = 1;
			}
		}
		// get data (revised)
		for (int i = 0; i < urls.size(); i++) {
			boolean done = false;
			int attempts = 1;
			while (!done) {
				try {
					extractData(i);
					done = true;
				} catch (Exception e) {
					System.out.println("attempt " + attempts + " failed");
					attempts++;
				}
			}
			System.out.println((i + 1) + "/" + urls.size());
		}
		// write output file
		System.out.println("Generating output...");
		BufferedWriter bw = new BufferedWriter(new FileWriter("statereopening_wapo_placesofworship.csv"));
		for (String state : states) {
			bw.write(state);
			bw.write(",");
			if (dateOpened.containsKey(state)) {
				bw.write(dateOpened.get(state));
			}
			bw.write(",");
			bw.write('\n');
		}
		bw.flush();
		bw.close();
		System.out.println("Done!");
	}
}