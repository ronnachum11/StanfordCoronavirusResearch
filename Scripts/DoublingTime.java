import java.io.*;
import java.util.*;

public class DoublingTime {
	static ArrayList<String> date;
	static ArrayList<Integer> hCumulative;
	//static ArrayList<Integer> hNew;
	static ArrayList<ArrayList<String>> getCovidTrackCSV(String inFile) throws Exception {
		ArrayList<ArrayList<String>> csvData = new ArrayList<ArrayList<String>>();
		BufferedReader br = new BufferedReader(new FileReader(inFile));
		String line = br.readLine();
		while (line != null) {
			Scanner sc = new Scanner(line).useDelimiter(",");
			ArrayList<String> arr = new ArrayList<String>();
			while (sc.hasNext()) {
				arr.add(sc.next());
			}
			csvData.add(arr);
			line = br.readLine();
			sc.close();
		}
		br.close();
		return csvData;
	}
	public static void main(String[] args) throws Exception {
		ArrayList<ArrayList<String>> csv = getCovidTrackCSV("az_covid_track_api_data.csv");
		date = new ArrayList<String>();
		hCumulative = new ArrayList<Integer>();
		//hNew = new ArrayList<Integer>();
		// get date and cumulative hospitalizations
		for (int i = 1; i < csv.size(); i++) {
			if (csv.get(i).isEmpty()) {
				break;
			}
			if (!csv.get(i).get(7).equals("")) {
				hCumulative.add(Integer.parseInt(csv.get(i).get(7)));
				date.add(csv.get(i).get(1));
			}
		}
		// reverse date and cumulative hospitalizations
		for (int i = 0; i < date.size() / 2; i++) {
			String temp1 = date.get(i);
			date.set(i, date.get(date.size() - i - 1));
			date.set(date.size() - i - 1, temp1);
			int temp2 = hCumulative.get(i);
			hCumulative.set(i, hCumulative.get(hCumulative.size() - i - 1));
			hCumulative.set(hCumulative.size() - i - 1, temp2);
		}
		/* determine hNew based on hCumulative
		hNew.add(hCumulative.get(0));
		for (int i = 1; i < hCumulative.size(); i++) {
			hNew.add(hCumulative.get(i) - hCumulative.get(i - 1));
		}
		*/
		// change output file name as needed
		BufferedWriter bw = new BufferedWriter(new FileWriter("July12ArizonaDoublingTime.txt"));
		for (int i = 7; i < date.size(); i++) {
			// doubling time calculated with the formula found here:
			// https://en.wikipedia.org/wiki/Doubling_time
			double change_in_time = 7;
			double ln_2 = Math.log(2);
			double q2 = hCumulative.get(i);
			double q1 = hCumulative.get(i - 7);
			double ln_q2_q1 = Math.log(q2 / q1);
			double doubling_time = change_in_time * ln_2 / ln_q2_q1;
			bw.write(date.get(i) + " " + doubling_time + '\n');
		}
		bw.flush();
		bw.close();
	}
}
