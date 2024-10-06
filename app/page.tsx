import dynamic from "next/dynamic";

// Update the import path to correctly point to the Map component
const Map = dynamic(() => import("./components/Map"), { ssr: false });

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">
            Spotted Lanternfly Map
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Maryland and Virginia Distribution
          </p>
        </header>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="mb-4">
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-2">
              Interactive Map
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              Explore the distribution of Spotted Lanternflies and Trees of
              Heaven in Maryland and Virginia.
            </p>
          </div>
          <div className="aspect-w-16 aspect-h-9">
            <Map />
          </div>
        </div>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
              About Spotted Lanternfly
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              The Spotted Lanternfly is an invasive pest that primarily feeds on
              tree of heaven but can also feed on a wide range of crops.
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
              Map Legend
            </h3>
            <ul className="list-disc list-inside text-gray-600 dark:text-gray-300">
              <li>Red markers: Spotted Lanternfly sightings</li>
              <li>Green markers: Tree of Heaven locations</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}
