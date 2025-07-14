import React from "react";

const teamMembers = [
  {
    name: "Elariz",
    role: "CS Student",
    img: "https://randomuser.me/api/portraits/men/36.jpg",
    profile: "#",
  },
  {
    name: "Alvin",
    role: "Software Engineer",
    img: "https://randomuser.me/api/portraits/men/37.jpg",
    profile: "#",
  },
  {
    name: "Aaryan",
    role: "ML Engineer",
    img: "https://randomuser.me/api/portraits/men/38.jpg",
    profile: "#",
  },
  {
    name: "Abdullah",
    role: "Computer Science",
    img: "https://randomuser.me/api/portraits/men/39.jpg",
    profile: "#",
  },
  {
    name: "Sok Leg Chan",
    role: "Software Engineer",
    img: "https://randomuser.me/api/portraits/men/40.jpg",
    profile: "#",
  },
  {
    name: "Sahana",
    role: "Software Engineer",
    img: "https://randomuser.me/api/portraits/women/36.jpg",
    profile: "#",
  },
  {
    name: "Vika",
    role: "Gen-AI Engineer",
    img: "https://randomuser.me/api/portraits/women/37.jpg",
    profile: "#",
  },
  {
    name: "Nicolas",
    role: "GenAI Consultant",
    img: "https://randomuser.me/api/portraits/men/41.jpg",
    profile: "#",
  },
];

export default function TeamSection() {
  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-2">
          The Minds Behind LawCo
        </h2>
        <p className="text-center text-gray-600 mb-10">
          Our dedicated team of innovators:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {teamMembers.map((member, idx) => (
            <div
              key={idx}
              className="bg-white rounded-2xl shadow-md p-6 flex flex-col items-center hover:shadow-lg transition-shadow"
            >
              <img
                src={member.img}
                alt={member.name}
                className="w-24 h-24 rounded-full border-4 border-blue-200 object-cover mb-4"
              />
              <h3 className="text-xl font-semibold mb-1 text-center">
                {member.name}
              </h3>
              <p className="text-gray-600 mb-4 text-center">{member.role}</p>
              <a
                href={member.profile}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors text-sm"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-5 h-5"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M17.25 6.75V6A2.25 2.25 0 0015 3.75h-6A2.25 2.25 0 006.75 6v12A2.25 2.25 0 009 20.25h6a2.25 2.25 0 002.25-2.25v-.75m-6-4.5l9-9m0 0v5.25m0-5.25H13.5"
                  />
                </svg>
                Profile
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
