import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.*;
import java.net.*;

public class MAIN {

    public static void printSystemInfo() {
        String osName = System.getProperty("os.name");
        String osVersion = System.getProperty("os.version");
        String osArch = System.getProperty("os.arch");
        String javaVersion = System.getProperty("java.version");
        String javaHome = System.getProperty("java.home");

        System.out.println("Operating System: " + osName);
        System.out.println("OS Version: " + osVersion);
        System.out.println("OS Architecture: " + osArch);
        System.out.println("Java Version: " + javaVersion);
        System.out.println("Java Home: " + javaHome);

        long totalMemory = Runtime.getRuntime().totalMemory() / (1024 * 1024); // MB
        long freeMemory = Runtime.getRuntime().freeMemory() / (1024 * 1024); // MB
        long maxMemory = Runtime.getRuntime().maxMemory() / (1024 * 1024); // MB

        System.out.println("Total Memory: " + totalMemory + " MB");
        System.out.println("Free Memory: " + freeMemory + " MB");
        System.out.println("Max Memory: " + maxMemory + " MB");
    }

    public static void printGeoLocation() {
        try {
            URL url = new URL("http://ipinfo.io/json");
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            String inputLine;
            StringBuilder content = new StringBuilder();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
            in.close();
            Gson gson = new GsonBuilder().setPrettyPrinting().create(); // 使用 PrettyPrinting
            JsonObject jsonObject = JsonParser.parseString(content.toString()).getAsJsonObject();
            String prettyJson = gson.toJson(jsonObject);
            System.out.println("Formatted Geo Location Data: ");
            System.out.println(prettyJson);
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Error fetching geo-location.");
        }
    }

    public static void main(String[] args) {
        printSystemInfo();
        printGeoLocation();
    }
}
