package com.zdiv.jlib.app.WebToon;

import java.io.File;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.zdiv.jlib.base.Encoding;
import com.zdiv.jlib.base.FileUtility;

public class WolfCom {
	
	final static boolean debug = false;
	final static String filter = null; //"jpg";
	
	public static Document getJsoupDocument(String url) throws InterruptedException {
		while( true ) {
			try {
				return Jsoup.connect(url).get();
			} catch ( Exception e ) {
				e.printStackTrace();
				Thread.sleep(1000);
			}
		}
	}


	public static void downloadFile(String urlStr, String fileName, String referer) throws IOException {
        URL url = new URL(urlStr);
        HttpURLConnection  hc = (HttpURLConnection) url.openConnection();
        hc.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36");
        hc.setRequestProperty("Referer", referer);
       
    	int status = hc.getResponseCode();
    	while (status != HttpURLConnection.HTTP_OK) {
    		if (status == HttpURLConnection.HTTP_MOVED_TEMP
    			|| status == HttpURLConnection.HTTP_MOVED_PERM
    			|| status == HttpURLConnection.HTTP_SEE_OTHER ) {
        		String newUrl = hc.getHeaderField("Location");
        		hc = (HttpURLConnection) new URL(newUrl).openConnection();
        		hc.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36");
            	status = hc.getResponseCode();
    		}
    		if (status == HttpURLConnection.HTTP_NOT_FOUND ) {
    			return;
    		}
    	}            
        
        Files.copy(hc.getInputStream(), Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
	}
	

	public static void getWolfCom(String comicsUrl, String baseUrl, String baseDir)  
			throws InterruptedException, MalformedURLException, IOException {

		Document doc_toc = getJsoupDocument(comicsUrl);
		if( debug ) {
			//String text = doc_toc.text();
			String html = doc_toc.html();
			System.out.println(html);
			FileUtility.StringToFile("D:/aa.html",html);
		}
		
		Elements list = doc_toc.select("div.box > div.group.left-box > div.webtoon-bbs-list.bbs-list > ul > li");
		if( debug ) {
			System.out.println(list.html());
		}
		
		File dir = new File(baseDir,doc_toc.title().replaceAll("[?/:]","_"));
		dir.mkdirs();
	
		int i = 0;
		for( Element e : list ) {
			
			//if( i++ < 33 ) continue;
			//if( ++i > 3 ) break;
			
			try {
				String url = baseUrl + e.select("a").first().attr("href");
				if( debug ) {
					System.out.println(url);
				}
				
				Document doc_img = getJsoupDocument(url);
				Elements imgs = doc_img.select("section.webtoon-body > div.group.image-view > img");
				System.out.println(doc_img.title());
				
				File subdir = new File(dir.getPath(),doc_img.title().replaceAll("[?/:]","_"));
				if( subdir.exists() ) {
					continue;
				} else {
					subdir.mkdirs();
				}
				
				int k = 1;
				for( Element img : imgs ) {
					String img_url = img.attr("src");
					if( filter == null || img_url.endsWith(filter) ) { 
						if( ! img_url.startsWith("http") ) {
							img_url = baseUrl + img_url;
						}
						String file_name = String.format("img_%04d.jpg",k++);
						System.out.println( img_url + " -> " + file_name );
						downloadFile(img_url,subdir.getPath() + "/" + file_name,comicsUrl);
					}
				}
			} catch( Exception e1 ){
			
			}
			//break;
		}
	}
	
	public static void main(String[] args) throws InterruptedException, MalformedURLException, IOException {
		String[] url = {
				//"https://wfwf104.com/list?toon=1229",
				"https://wfwf105.com/list?toon=381&title=%B8%BE%C4%AB%C6%E4",
			};
		String iurl = "https://wfwf105.com";
		String dir = "D:/Temp4/";
		for( String u : url ) {
			getWolfCom(u, iurl, dir);
			System.out.println( "END" );
		}
	}
}
