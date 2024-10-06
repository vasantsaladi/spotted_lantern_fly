"use client";

import { useState } from "react";

const Map = () => {
  const [isLoading, setIsLoading] = useState(true);

  return (
    <div className="space-y-4">
      <div className="w-full h-[600px] bg-gray-200 rounded-lg relative">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-gray-500">Loading map...</p>
          </div>
        )}
        <iframe
          src="/maryland_virginia_flies_and_trees.html"
          className="w-full h-full border-none"
          onLoad={() => setIsLoading(false)}
        />
      </div>
    </div>
  );
};

export default Map;
