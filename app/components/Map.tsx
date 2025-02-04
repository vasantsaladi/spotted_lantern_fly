"use client";

import { useEffect, useRef, useState } from "react";

const Map = () => {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let view: __esri.MapView;

    const loadMap = async () => {
      try {
        const [Map, MapView] = await Promise.all([
          import("@arcgis/core/Map"),
          import("@arcgis/core/views/MapView"),
        ]);

        const map = new Map.default({
          basemap: "streets-navigation-vector",
        });

        view = new MapView.default({
          container: mapRef.current as HTMLDivElement,
          map: map,
          center: [-77.0369, 38.9072], // Longitude, latitude for Washington, D.C.
          zoom: 10,
        });

        view.when(() => {
          setIsLoading(false);
        });
      } catch (error) {
        console.error("Error loading ArcGIS map:", error);
      }
    };

    loadMap();

    return () => {
      if (view) {
        view.destroy();
      }
    };
  }, []);

  return (
    <div className="space-y-4">
      <div className="w-full h-[600px] bg-gray-200 rounded-lg relative">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-gray-500">Loading map...</p>
          </div>
        )}
        <div ref={mapRef} className="w-full h-full"></div>
      </div>
    </div>
  );
};

export default Map;
