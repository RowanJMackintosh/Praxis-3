// Copyright 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package com.example.mapwithmarker;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.BitmapDescriptor;

import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Marker;


import com.google.android.gms.maps.model.LatLngBounds;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;

import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;



class Bin {
    public double latitude;
    public double longitude;
    public String title;
    public int weight;
    public boolean full;
    Marker marker;

    public Bin(double latitude, double longitude, String title, int weight, boolean full) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.title = title;
        this.weight = weight;
        this.full = full;
        this.marker = null;
    }

    public void add_marker(Marker marker){
        this.marker = marker;
    }

    public void delete_marker(Marker marker){
        this.marker = null;
    }
}

class BinList {
    //public OneMarker[] markers;
    public List<Bin> bins;
    LatLng user_pos = new LatLng(43.66005, -79.3967);

    public BinList() {
        //markers = new  OneMarker[size];
        bins = new ArrayList<>();
    }

    public Bin add(double latitude, double longitude, int weight, boolean full){
        String title = makeTitle(weight, full);
        Bin bin = new Bin(latitude, longitude, title, weight, full);
        bins.add(bin);

        return bin;
    }

    public String makeTitle(int weight, boolean full) {
        String fullState = full ? "full": "not full";
        return "W: "+weight/1000+"kg, "+fullState;
    }

    public Bin findBin(double latitude, double longitude){
        for (Bin bin_ : bins) {
            if (bin_.latitude == latitude && bin_.longitude == longitude)
                return bin_;
        }

        return null;
    }

    public LatLngBounds boundingBox(){
        LatLngBounds.Builder builder = new LatLngBounds.Builder();
        // This is a hack for now to include a user position in the bounding box. To be replaced by actual user later
        builder.include(user_pos);

        for(Bin aBin : bins) {
            builder.include(new LatLng(aBin.latitude, aBin.longitude));
        }
        return builder.build();
    }
}



/**
 * An activity that displays a Google map with a marker (pin) to indicate a particular location.
 */
public class MapsMarkerActivity extends AppCompatActivity
        implements OnMapReadyCallback, GoogleMap.OnMapClickListener, GoogleMap.OnMarkerClickListener
{

    private final String myTag = "MyTag";
    private GoogleMap mMap;

    int padding = 100; // This should be relative, but leave for now
    LatLngBounds bounds;
    BinList myBinList;

    // DEFAULT IP of the emulator
    static String SERVER_IP = "10.0.2.15";
    static final int SERVER_PORT = 18080;
    //private Handler handler = new Handler();
    ServerSocket serverSocket;


    class StartupThread implements Runnable {
        String name;
        public StartupThread(String name) {
            super();
            this.name = name;
        }

        @Override
        public void run() {
            //BitmapDescriptor greenIcon = BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN);
            BitmapDescriptor cyanIcon = BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_CYAN);
            BitmapDescriptor redIcon = BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED);


            List<Bin> tempBins = new ArrayList<>();
            tempBins.add(new Bin(43.6632, -79.38315, "1", 1001,false));
            tempBins.add(new Bin(43.6619, -79.3995, "2",2000,false));
            tempBins.add(new Bin(43.65228, -79.3914, "3", 10000,true));

            // Add markers for each of the bins
            for(Bin bin_ : tempBins){
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }

                Bin bin = myBinList.add(bin_.latitude, bin_.longitude, bin_.weight,bin_.full);

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Marker marker = mMap.addMarker(new MarkerOptions()
                                .position(new LatLng(bin.latitude, bin.longitude))
                                .title(bin.title)
                                .icon(bin.full ? redIcon : cyanIcon));
                        bin.add_marker(marker);

                        bounds = myBinList.boundingBox();
                        mMap.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds, padding));
                    }
                });
            }

        }
    }



    class ServerThread implements Runnable {
        String name;
        //BitmapDescriptor greenIcon = BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN);
        BitmapDescriptor cyanIcon = BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_CYAN);
        BitmapDescriptor redIcon = BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED);
        public ServerThread(String name) {
            super();
            this.name = name;
        }

        @Override
        public void run() {
            try {
                // Set up socket for client connections to come to
                serverSocket = new ServerSocket(SERVER_PORT);

                while (true) {
                    // Listen for incoming client connections
                    Log.d(myTag,"Listening for client on IP "+SERVER_IP + ":"+SERVER_PORT);
                    Socket client = serverSocket.accept();

                    // Have a client connection. read and process the data.
                    Log.d(myTag,"Client connected.");
                    try {
                        BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));

                        // read in the character stream from the client and parse it
                        String line = in.readLine();
                        Log.d(myTag,"Client sent line of data. data:" + line);

                        // There should be only one line sent per update. If more this is an error!
                        String line2  = in.readLine();
                        if (line2 != null) {
                            Log.d(myTag,"ERROR: Client sent more than one line of data. data:" + line2);
                            client.close();
                            continue;
                        }

                        // Process input
                        //String line_str = new String(line, StandardCharsets.UTF_8);
                        String[] tokens = line.split(" ");
                        if (tokens.length != 4) {
                            Log.d(myTag,"ERROR: Client sent other than 4 words in data.");
                            continue;
                        }

                        double latitude = Double.parseDouble(tokens[0]);
                        double longitude = Double.parseDouble(tokens[1]);
                        int weight = Integer.parseInt(tokens[2]);
                        boolean full = Boolean.parseBoolean(tokens[3]);

                        Bin bin_ = myBinList.findBin(latitude, longitude);

                        if (bin_ != null){
                            // we found a bin and need to update it
                            Marker marker = bin_.marker;
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    // Update the existing marker
                                    marker.setPosition(new LatLng(latitude, longitude));
                                    marker.setTitle(myBinList.makeTitle(weight, full));
                                    marker.setIcon(full ? redIcon : cyanIcon);

                                    bounds = myBinList.boundingBox();
                                    mMap.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds, padding));
                                }
                            });

                        } else {
                            // There is no bin and we need to make a new one
                            Bin bin = myBinList.add(latitude, longitude, weight, full);

                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {

                                    Marker marker = mMap.addMarker(new MarkerOptions()
                                            .position(new LatLng(bin.latitude, bin.longitude))
                                            .title(bin.title)
                                            .icon(bin.full ? redIcon : cyanIcon));
                                    bin.add_marker(marker);

                                    bounds = myBinList.boundingBox();
                                    mMap.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds, padding));
                                }
                            });
                        }
                    } catch (Exception e) {
                        Log.d(myTag, "Connection interrupted.");
                        Log.e(myTag, "IO exception", e);
                    }
                }
            } catch (IOException e) {
                Log.d(myTag, "IO exception in Server thread");
                Log.e(myTag, "IO exception", e);
            }
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        try {
            // MAKE SURE YOU CLOSE THE SOCKET UPON EXITING
            serverSocket.close();
        } catch (IOException e) {
            Log.d(myTag, "IO exception in Server thread");
            Log.e(myTag, "IO exception", e);
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Retrieve the content view that renders the map.
        setContentView(R.layout.activity_maps);

        // Get the SupportMapFragment and request notification when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    /**
     * Manipulates the map when it's available.
     * The API invokes this callback when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user receives a prompt to install
     * Play services inside the SupportMapFragment. The API invokes this method after the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        // Add a marker in Sydney, Australia,
        // and move the map's camera to the same location.

        mMap = googleMap;
        mMap.setOnMapClickListener(this);
        //mMap.setOnMapLongClickListener(this);
        mMap.setOnMarkerClickListener(this);


        // Make up a list of bins
        myBinList = new BinList();

        bounds = myBinList.boundingBox();

        googleMap.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds, padding));

        new Thread(new StartupThread("StartupThread")).start();

        // Start the network server  thread
        //SERVER_IP = getLocalIpAddress();    This is currently hardcoded to the emulators IP!
        new Thread(new ServerThread("serverThread")).start();
    }



    @Override
    public void onMapClick(@NonNull LatLng point){
        Log.d(myTag, "!!!!!!!!! Map clicked !!!!!!!!");

        bounds = myBinList.boundingBox();
        mMap.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds, padding));
    }

    /* Called when the user clicks a marker. */
    @Override
    public boolean onMarkerClick(@NonNull final Marker marker) {

        Log.d(myTag, "!!!!!!!!! Marker clicked !!!!!!!!");

        return false;
    }




}

