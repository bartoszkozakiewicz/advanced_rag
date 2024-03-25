import { FC } from "react";
import Image from "next/image";
import { StaticImageData } from "next/image";

interface Props {
  img: StaticImageData;
  price: number;
  description: string;
}

const RecommendItem: FC<Props> = ({ img, price, description }) => {
  return (
    <div className="mx-1 mb-10 w-5/12 cursor-pointer rounded-lg border-2 bg-white hover:bg-gray-200 md:w-1/4 lg:w-1/5 xl:w-1/6">
      <div className="mb-5 flex justify-center">
        <Image
          src={img}
          className="b-2 w-full px-8 pt-4"
          alt="recommended_item"
        />
      </div>
      <div className="px-5">
        <h6 className="text-xl font-bold">${price}</h6>
        <p className="mt-1 mb-3 text-sm text-[#8B96A5] md:text-base">
          {description}
        </p>
      </div>
    </div>
  );
};

export default RecommendItem;
