import java.io.*;
import java.net.*;
import java.util.*;

public class StateReopeningSpreadsheet {

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
	// keywords.get(column number) = a list of keywords corresponding to the given spreadsheet column
	// ex. "nail", "tattoo", and "massage" correspond to the column for non-hair personal care
	// earlier columns have priority over later columns: for example, if a phrase contains keywords for 
	// both curbside pickup retail and normal retail, then the phrase represents curbside pickup retail
	static ArrayList<ArrayList<String>> keywords;
	// stores spreadsheet before a CSV file is made
	// cells.get([state name]).get([column number]) = dates at given row and column
	static HashMap<String, HashMap<Integer, ArrayList<String>>> cells;
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
					category = category.toLowerCase();
					info = info.toLowerCase();
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
		// initialize keywords
		keywords = new ArrayList<ArrayList<String>>();
		// restaurants (outdoor dining only)
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("outdoor dining");
		// restaurants and bars
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("bars");
		// dine-in restaurants, no bars
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("restaurant");
		// retail (curbside pickup only)
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("retail open to curbside");
		keywords.get(keywords.size() - 1).add("stores open to curbside");
		keywords.get(keywords.size() - 1).add("retail open to pickup");
		keywords.get(keywords.size() - 1).add("stores open to pickup");
		// indoor retail
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("retail");
		// hair salons and barbershops
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("hair");
		keywords.get(keywords.size() - 1).add("barber");
		// non-hair personal care
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("nail");
		keywords.get(keywords.size() - 1).add("tattoo");
		keywords.get(keywords.size() - 1).add("massage");
		keywords.get(keywords.size() - 1).add("tanning");
		keywords.get(keywords.size() - 1).add("cosmetology");
		// gyms and fitness centers
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("gym");
		keywords.get(keywords.size() - 1).add("fitness");
		// entertainment
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("bowling");
		keywords.get(keywords.size() - 1).add("movie");
		keywords.get(keywords.size() - 1).add("entertainment");
		// houses of worship (ADDITIONAL CODE BELOW)
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("worship");
		keywords.get(keywords.size() - 1).add("religious");
		// office enviroments
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("office");
		// construction
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("construction");
		keywords.get(keywords.size() - 1).add("distribution");
		// beaches
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("beach");
		// state parks
		keywords.add(new ArrayList<String>());
		keywords.get(keywords.size() - 1).add("state park");
		keywords.get(keywords.size() - 1).add("state camp");
		keywords.get(keywords.size() - 1).add("campground");
		//debug
		//System.out.println(keywords);
		// initialize urls
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
		int endDay = 16;
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
		// initialize cells
		cells = new HashMap<String, HashMap<Integer, ArrayList<String>>>();
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
			cells.put(state, new HashMap<Integer, ArrayList<String>>());
			for (int i = 0; i < keywords.size(); i++) {
				cells.get(state).put(i, new ArrayList<String>());
			}
			for (int i = 1; i < urls.size(); i++) {
				HashMap<String, String> curr = data.get(state).get(urls.get(i));
				HashMap<String, String> prev = data.get(state).get(urls.get(i - 1));
				// contains all NYTimes categories found in either the current day or the previous day (or both)
				// do NOT confuse with spreadsheet columns
				HashSet<String> categories = new HashSet<String>();
				categories.addAll(curr.keySet());
				categories.addAll(prev.keySet());
				// currHas[column number] = whether the given spreadsheet column is represented in current day's data
				// prevHas[column number] = whether the given spreadsheet column is represented in previous day's data
				boolean[] currHas = new boolean[keywords.size()];
				boolean[] prevHas = new boolean[keywords.size()];
				for (String category : categories) {
					// determine currHas
					if (curr.containsKey(category)) {
						// look at all phrases in the current day and the given category
						Scanner sc = new Scanner(curr.get(category)).useDelimiter(",|;");
						while (sc.hasNext()) {
							String phrase = sc.next();
							boolean found = false;
							for (int col = 0; col < keywords.size(); col++) {
								for (String keyword : keywords.get(col)) {
									// if phrase contains a keyword
									if (phrase.contains(keyword)) {
										found = true;
										currHas[col] = true;
									}
									if (curr.get(category).equals("[no info]") && category.contains(keyword)) {
										found = true;
										currHas[col] = true;
									}
								}
								// avoid representing more than one column per phrase
								if (found) {
									break;
								}
							}
						}
						sc.close();
					}
					// determine prevHas
					if (prev.containsKey(category)) {
						Scanner sc = new Scanner(prev.get(category)).useDelimiter(",|;");
						while (sc.hasNext()) {
							String phrase = sc.next();
							boolean found = false;
							for (int col = 0; col < keywords.size(); col++) {
								for (String keyword : keywords.get(col)) {
									if (phrase.contains(keyword)) {
										found = true;
										prevHas[col] = true;
									}
									if (prev.get(category).equals("[no info]") && category.contains(keyword)) {
										found = true;
										prevHas[col] = true;
									}
								}
								if (found) {
									break;
								}
							}
						}
						sc.close();
					}
				}
				// compare currHas and prevHas, update cells accordingly
				for (int col = 0; col < keywords.size(); col++) {
					// if given column goes from unrepresented to represented (i.e. hair salons opening), or
					// if given column goes from represented to unrepresented (i.e. hair salons closing)
					if (currHas[col] != prevHas[col]) {
						// get month-day date corresponding to current url
						String date = urls.get(i).substring(
								"https://web.archive.org/web/2020".length(), 
								"https://web.archive.org/web/2020".length() + 4);
						// add date to spreadsheet
						cells.get(state).get(col).add(date);
					}
				}
			}
			// debug
			//System.out.println(state);
			//System.out.println("cells for this state: " + cells.get(state));
		}
		// make csv file based on cells
		BufferedWriter bw = new BufferedWriter(new FileWriter("statereopening.csv"));
		for (String state : states) {
			bw.write(state);
			for (int col = 0; col < keywords.size(); col++) {
				bw.write(",");
				for (int i = 0; i < cells.get(state).get(col).size(); i++) {
					String date = cells.get(state).get(col).get(i);
					if (i > 0) {
						bw.write(" ");
					}
					bw.write(date);
				}
			}
			bw.write('\n');
		}
		bw.flush();
		bw.close();
		System.out.println("Done!");
	}
}