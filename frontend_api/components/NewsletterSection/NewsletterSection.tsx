"use client";

import React from "react";

type Props = {};

const NewsletterSection = (props: Props) => {
  return (
    <div className="bg-[#E0E0E0] py-10 md:py-20">
      <h4 className="py-0 text-center text-2xl font-bold tracking-wide md:py-1 md:text-3xl">
        Subscribe on our newsletter
      </h4>
      <p className="mt-1 mb-5 text-center text-sm text-[#606060] md:text-lg">
        Get daily news on upcoming offers from many suppliers all over the
        world!
      </p>

      <div className="flex justify-center">
        <input
          type="email"
          placeholder="Enter your email here..."
          className="w-2/5 rounded-lg border-2 p-2 text-[#8B96A5] caret-[#8B96A5] outline-none transition-all hover:border-blue-600"
        />

        <button className="ml-2 flex w-1/12 items-center justify-center rounded-lg bg-gradient-to-b from-[#127FFF] to-[#0067FF] px-16 text-center text-sm font-normal tracking-wider text-white outline-none transition-all duration-700 hover:-translate-y-1 md:ml-5 md:p-2 md:px-5 md:text-xs lg:ml-10 lg:p-0 lg:text-sm">
          Subscribe
        </button>
      </div>
    </div>
  );
};

export default NewsletterSection;
