package tfidf;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import javax.xml.crypto.dsig.spec.TransformParameterSpec;

import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

import code.NlpirTest;

public class TFIDF {
	//存储单个文件tf值
	static Map <String, Map <String, Integer>> tfMap = new HashMap<String, Map <String, Integer>>();
	//存储所有文件的单词出现情况
	static Map <String, Integer > tfMapaLL = new HashMap<String , Integer>();
	//存储idf值
	static Map <String, Map <String, Integer>> idfMap = new HashMap<String, Map <String, Integer>>();
	//存储最终的tfidf值
	static Map <String, Map <String, Double>> tfidfMap = new HashMap<String, Map <String, Double>>();
	static int fileNum=0;

	public static void main(String[] args){

		//遍历文件夹，生成所有文件的map
		String path = "E:/testFile"; // 路径
        File f = new File(path);
        if (!f.exists()) {
            System.out.println(path + " not exists");
            return;
        }
        File fa[] = f.listFiles();
        fileNum=fa.length;
        for (int i = 0; i < fa.length; i++) {
            File fs = fa[i];
            if (!fs.isDirectory()) {
							//key为文件名，value为每个文件的tf/idf值，下面会看到value也是一个新的map
            	tfMap.put(fs.getName(),null);
            	idfMap.put(fs.getName(),null);
            	tfidfMap.put(fs.getName(),null);
            } else {
            	System.out.println(fs.getName() + " [目录]");
            }
        }

        String tmpFileString="";
        String sOutputString="";
        Map <String, Integer> tmpMap=new HashMap<String, Integer>();
        Map <String, Integer> tmpMap1=new HashMap<String, Integer>();
        //计算每个文件的tf值
        for (String key : tfMap.keySet()) {
        	//读每个文件生成文件字符串
        	tmpFileString=readFileByLines("E:/testFile/"+key);
        	tmpMap=new HashMap<String, Integer>();
        	tmpMap1=new HashMap<String, Integer>();
        	//每个文件分词把tfMap生成
    		try {
    			//System.out.println(tmpFileString);
    			sOutputString = NlpirTest.nlpir(tmpFileString);
					//调用分词工具生成每个文件的词字符串数组
    			String[]  strs=sOutputString.split("/([a-z]*)\\d*\\s");
    			for(int i=0,len=strs.length;i<len;i++){
    			    //System.out.println(strs[i].toString());
							//遍历每个文件 如果有这个词 词出现的次数+1 否则第一次出现次数设置为1
							//mapall为所有词的个数
    				if(tfMapaLL.containsKey(strs[i].toString())){
    					tfMapaLL.put(strs[i].toString(), tfMapaLL.get(strs[i].toString())+1);
    				}else{
    					tfMapaLL.put(strs[i].toString(),1);
    				}

						//tmpmap为每个文件的tf值
    				if(tmpMap.containsKey(strs[i].toString())){
    					tmpMap.put(strs[i].toString(), tmpMap.get(strs[i].toString())+1);
    				}else{
    					tmpMap.put(strs[i].toString(),1);
    				}
						//将idf初始值先都初始化为0
    				tmpMap1.put(strs[i].toString(),0);
    			}
    			tfMap.put(key,tmpMap);
    			idfMap.put(key, tmpMap1);
    		} catch (Exception e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		}
        }

        System.out.println(tfMap);

        //根据tfMap生成idfMap 两层循环遍历
        for (String key : tfMap.keySet()) {
        	//System.out.println(tmpMap.get("fsad"));
        	for (String key1 : tfMap.keySet()) {
            	//System.out.println(tmpMap.get("fsad"));
        		tmpMap1=idfMap.get(key);
        		tmpMap=tfMap.get(key1);
        		for(String key2:tmpMap1.keySet()){
        			//System.out.println(key2);
							//如果一个文件有该词 idf+1
        			if(tmpMap.containsKey(key2)){
        				tmpMap1.put(key2, tmpMap1.get(key2)+1);
        			}
        		}
        		idfMap.put(key, tmpMap1);
            }
        }
        System.out.println(idfMap);

        //根据tfMap，idfMap生成tfIdfMap 按word中公式计算生成
        Map <String, Double> tmpMap2=new HashMap<String, Double>();
        for (String key : tfMap.keySet()){
        	tmpMap=tfMap.get(key);
        	tmpMap1=idfMap.get(key);
        	tmpMap2=new HashMap<String, Double>();
        	for(String key1:tmpMap.keySet()){
        		//System.out.println(tmpMap.get(key1));
        		//System.out.println(key1+tfMapaLL.get(key1));
        		//tf值
        		double tfValue=tmpMap.get(key1)*1.0/tfMapaLL.get(key1)*1.0;
        		//idf值
        		double idfValue=Math.log(fileNum*1.0/(1+tmpMap1.get(key1))*1.0);
        		//System.out.println(tmpMap1.get(key1));
        		//System.out.println(tfValue+" "+idfValue);
        		tmpMap2.put(key1,tfValue*idfValue);
        	}
        	tfidfMap.put(key, tmpMap2);
        }

        System.out.println(tfidfMap);

        //排序并输出 tfidf
        List<Map.Entry<String,Double>> list;
        for (String key : tfidfMap.keySet()){
        	System.out.println(key);
        	tmpMap2=tfidfMap.get(key);
        	 list = new ArrayList<Map.Entry<String,Double>>(tmpMap2.entrySet());
        	 Collections.sort(list,new Comparator<Map.Entry<String,Double>>() {
                 //升序排序
                 public int compare(Entry<String, Double> o1,
                         Entry<String, Double> o2) {
                     return o2.getValue().compareTo(o1.getValue());
                 }
             });

						 //输出
             for(Entry<String, Double> mapping:list){
            	 if(mapping.getValue()>0.3){
            		 System.out.println(mapping.getKey()+":"+mapping.getValue());
            	 }else{
            		 break;
            	 }
               }
        }
	}

	private static String readFileByLines(String fileName) {
        File file = new File(fileName);
        String fileString="";
        BufferedReader reader = null;
        try {
            //System.out.println("以行为单位读取文件内容，一次读一整行：");
            reader = new BufferedReader(new FileReader(file));
            String tempString = null;
            int line = 1;
            // 一次读入一行，直到读入null为文件结束
            while ((tempString = reader.readLine()) != null) {
                // 显示行号
            	fileString+=tempString;
                //System.out.println("line " + line + ": " + tempString);
                line++;
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e1) {
                }
            }
        }
        return fileString;
    }

}
