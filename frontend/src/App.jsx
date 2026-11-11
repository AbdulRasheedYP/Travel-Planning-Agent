
import { useState } from "react";

function App() {
  const [form, setForm] = useState({
    starting_location: "",
    destination: "",
    budget: "",
    duration: "",
    travelers: "",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const inputStyle =
    "w-full rounded-lg border border-gray-200 bg-white px-4 py-3.5 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100";

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/generate-trip/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(form),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        const message =
          typeof data.error === "string"
            ? data.error
            : data.error?.message || "Unable to generate travel plan.";

        throw new Error(message);
      }

      if (!data.success) {
        throw new Error("Unable to generate travel plan.");
      }

      setResult(data);

      setTimeout(() => {
        document.getElementById("results")?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function resetForm() {
    setResult(null);
    setError("");

    setForm({
      starting_location: "",
      destination: "",
      budget: "",
      duration: "",
      travelers: "",
    });

    document.getElementById("planner")?.scrollIntoView({
      behavior: "smooth",
    });
  }

  return (
    <main className="min-h-screen bg-white text-gray-900">

      {/* Navbar */}
      <nav className="sticky top-0 z-50 border-b border-gray-100 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <a href="#home" className="text-2xl font-bold tracking-tight">
            Travel<span className="text-blue-600">AI</span>
          </a>

          <div className="hidden items-center gap-9 text-sm font-medium text-gray-600 md:flex">
            <a href="#home" className="hover:text-blue-600">
              Home
            </a>

            <a href="#planner" className="hover:text-blue-600">
              Plan Your Trip
            </a>

            <a href="#about" className="hover:text-blue-600">
              About
            </a>
          </div>

          <a
            href="#planner"
            className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
          >
            Get Started
          </a>

        </div>
      </nav>

      {/* Hero */}
      <section
        id="home"
        className="relative flex min-h-[520px] items-center bg-cover bg-center px-6 py-24"
        style={{
          backgroundImage:
            "linear-gradient(rgba(10, 25, 45, 0.25), rgba(10, 25, 45, 0.45)), url('https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=2000&q=85')",
        }}
      >
        <div className="mx-auto w-full max-w-7xl">

          <div className="max-w-2xl text-white">

            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-white/90">
              Discover the beauty of travel
            </p>

            <h1 className="mt-6 text-4xl font-bold leading-tight sm:text-5xl md:text-6xl">
              Discover Your
              <br />
              Next Destination.
            </h1>

            <p className="mt-6 max-w-xl text-base leading-8 text-white/90 md:text-lg">
              Find beautiful destinations, explore new experiences
              and create a travel plan that fits your preferences.
            </p>

            <a
              href="#planner"
              className="mt-9 inline-block rounded-lg bg-white px-7 py-4 text-sm font-bold text-gray-900 transition hover:bg-gray-100"
            >
              Plan Your Journey
            </a>

          </div>
        </div>
      </section>

      {/* Introduction */}
      <section className="px-6 py-16">
        <div className="mx-auto max-w-4xl text-center">

          <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
            Travel Made Simple
          </p>

          <h2 className="mt-4 text-3xl font-bold md:text-4xl">
            Every Journey Begins With a Plan
          </h2>

          <p className="mx-auto mt-5 max-w-2xl leading-8 text-gray-500">
            Tell us where you want to go, how much you want to spend
            and how long you plan to travel. Get a personalized
            itinerary for your next journey.
          </p>

        </div>
      </section>

      {/* Planner Form */}
      <section id="planner" className="scroll-mt-24 bg-gray-50 px-6 py-20">

        <div className="mx-auto max-w-3xl">

          <div className="mb-10 text-center">

            <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
              Start Planning
            </p>

            <h2 className="mt-3 text-3xl font-bold">
              Plan Your Perfect Trip
            </h2>

            <p className="mt-3 text-gray-500">
              Enter your travel details below.
            </p>

          </div>

          <form
            onSubmit={handleSubmit}
            className="space-y-6 rounded-2xl border border-gray-100 bg-white p-6 shadow-sm md:p-10"
          >

            <div className="grid gap-6 md:grid-cols-2">

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Starting Location
                </label>

                <input
                  name="starting_location"
                  type="text"
                  placeholder="Enter starting location"
                  required
                  value={form.starting_location}
                  onChange={handleChange}
                  className={inputStyle}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Destination
                </label>

                <input
                  name="destination"
                  type="text"
                  placeholder="Enter destination"
                  required
                  value={form.destination}
                  onChange={handleChange}
                  className={inputStyle}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Total Budget (₹)
                </label>

                <input
                  name="budget"
                  type="number"
                  min="1"
                  placeholder="Enter your budget"
                  required
                  value={form.budget}
                  onChange={handleChange}
                  className={inputStyle}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Duration (Days)
                </label>

                <input
                  name="duration"
                  type="number"
                  min="1"
                  placeholder="Number of days"
                  required
                  value={form.duration}
                  onChange={handleChange}
                  className={inputStyle}
                />
              </div>

              <div className="md:col-span-2">
                <label className="mb-2 block text-sm font-semibold">
                  Number of Travellers
                </label>

                <input
                  name="travelers"
                  type="number"
                  min="1"
                  placeholder="Number of people"
                  required
                  value={form.travelers}
                  onChange={handleChange}
                  className={inputStyle}
                />
              </div>

            </div>

            {error && (
              <div className="rounded-lg border border-red-100 bg-red-50 p-4 text-sm text-red-600">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-blue-600 py-4 text-sm font-bold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading
                ? "Preparing Your Travel Plan..."
                : "Generate Travel Plan"}
            </button>

            <p className="text-center text-xs text-gray-400">
              Enter your details to create a personalized itinerary.
            </p>

          </form>

        </div>
      </section>

      {/* Results */}
      {result && result.success && (
        <section
          id="results"
          className="scroll-mt-24 px-6 py-20"
        >

          <div className="mx-auto max-w-6xl">

            <div className="mb-10">

              <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
                Your Travel Itinerary
              </p>

              <h2 className="mt-3 text-3xl font-bold">
                {result.itinerary.trip_title}
              </h2>

              <p className="mt-3 text-gray-500">
                Your personalized day-wise travel schedule.
              </p>

            </div>

            {/* Day Cards */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

              {result.itinerary.days.map((day) => (
                <article
                  key={day.day}
                  className="rounded-xl border border-gray-200 bg-white p-6 transition hover:shadow-md"
                >

                  <p className="text-sm font-bold tracking-wider text-blue-600">
                    DAY {day.day}
                  </p>

                  <h3 className="mt-4 text-xl font-bold leading-snug">
                    {day.title}
                  </h3>

                  <ul className="mt-5 space-y-4">

                    {day.activities.map((activity, index) => (
                      <li
                        key={index}
                        className="border-b border-gray-100 pb-3 text-sm leading-6 text-gray-600 last:border-0"
                      >
                        {activity}
                      </li>
                    ))}

                  </ul>

                </article>
              ))}

            </div>

            {/* Weather */}
            {result.weather && (
              <div className="mt-10 rounded-xl bg-slate-900 p-8 text-white">

                <h3 className="text-xl font-bold">
                  Weather Information
                </h3>

                <p className="mt-2 text-sm text-gray-400">
                  Latest weather data returned by the weather service.
                </p>

                <div className="mt-8 grid grid-cols-2 gap-6 md:grid-cols-4">

                  <div>
                    <p className="text-sm text-gray-400">Temperature</p>
                    <p className="mt-2 text-2xl font-bold">
                      {result.weather.temperature_2m}°C
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-400">Humidity</p>
                    <p className="mt-2 text-2xl font-bold">
                      {result.weather.relative_humidity_2m}%
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-400">Wind Speed</p>
                    <p className="mt-2 text-2xl font-bold">
                      {result.weather.wind_speed_10m} km/h
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-400">Precipitation</p>
                    <p className="mt-2 text-2xl font-bold">
                      {result.weather.precipitation} mm
                    </p>
                  </div>

                </div>
              </div>
            )}

            {/* Warnings */}
            {result.warnings?.length > 0 && (
              <div className="mt-6 rounded-lg border border-amber-200 bg-amber-50 p-5">
                <h3 className="font-bold text-amber-800">
                  Travel Notices
                </h3>

                <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-amber-700">
                  {result.warnings.map((warning, index) => (
                    <li key={index}>{warning}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-10 text-center">
              <button
                type="button"
                onClick={resetForm}
                className="rounded-lg border border-blue-600 px-7 py-3 font-semibold text-blue-600 transition hover:bg-blue-50"
              >
                Plan Another Trip
              </button>
            </div>

          </div>
        </section>
      )}

      {/* About */}
      <section id="about" className="bg-gray-50 px-6 py-16">

        <div className="mx-auto max-w-3xl text-center">

          <h2 className="text-2xl font-bold">
            About TravelAI
          </h2>

          <p className="mt-4 leading-8 text-gray-500">
            A simple travel planning platform designed to help
            travellers organize their journeys with personalized
            itineraries and destination weather information.
          </p>

        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 bg-white px-6 py-8">

        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 sm:flex-row">

          <h3 className="text-xl font-bold">
            Travel<span className="text-blue-600">AI</span>
          </h3>

          <p className="text-sm text-gray-500">
            Your journey, your way.
          </p>

          <p className="text-xs text-gray-400">
            © {new Date().getFullYear()} TravelAI. All rights reserved.
          </p>

        </div>

      </footer>

    </main>
  );
}

export default App;
