"use client";

import React, { FC, ReactElement } from "react";
import { useRouter } from "next/navigation";
interface Props {
  title: string;
  icon: ReactElement;
}

const NavBarButton: FC<Props> = ({ title, icon }) => {
  const router = useRouter();
  return (
    <div>
      <button
        className="px-3 text-[#8B96A5] transition-all hover:rounded-full hover:text-[#0D6EFD] xl:px-4"
        onClick={() => router.push("/cart_summary")}
      >
        {icon}
        <p className="xl:text-base">{title}</p>
      </button>
    </div>
  );
};

export default NavBarButton;
