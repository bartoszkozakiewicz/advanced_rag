"use client";

import CategoryItem from "@/components/CategorySection/CategoryItem/CategoryItem";
import React from "react";
import {
  CategoryImg1,
  CategoryImg2,
  Sofa,
  SoftChair,
  Chair,
  Pot,
  Mixer,
  Blender,
  Appliance,
  Plant,
  Watch,
  Camera,
  Headphone1,
  Headphone2,
  Kettle,
  Laptop,
  Tablet,
  Phone2,
} from "../../utils/CategoryAssets";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";

const page = () => {
  const [open, setOpen] = React.useState(false);

  return (
    <div className="flex justify-center">
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Porównanie produktów</DialogTitle>
        <DialogContent></DialogContent>
        <DialogActions>
          <button
            className="focus:shadow-outline mt-8 rounded bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700 focus:outline-none"
            type="button"
            onClick={() => setOpen(false)}
          >
            Thanks
          </button>{" "}
        </DialogActions>
      </Dialog>
      <div className="flex flex-col items-center">
        <p className="mb-8 mt-8 text-xl font-bold">Cart Summary</p>
        <div className="flex flex-row justify-between gap-[50px]">
          <div className="w-1/2 pr-8">
            {/* Produkty */}
            <div className="mb-8 flex flex-col items-center">
              <div className="mb-[800px] flex w-[500px] flex-col items-center ">
                <p className="text-xl font-bold">Cart Summary</p>
                <div className=" w-4/5 flex-1 ">
                  <CategoryItem
                    productImg1={Blender}
                    productImg2={Mixer}
                    productTitle1={"Blender"}
                    productTitle2={"Mixer"}
                    productPrice1={20}
                    productPrice2={30}
                  />
                </div>
                <button
                  className="focus:shadow-outline mt-8 rounded bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700 focus:outline-none"
                  type="button"
                  onClick={() => setOpen(true)}
                >
                  Compare products
                </button>
              </div>
            </div>
          </div>
          <div className="w-1/2">
            {/* Formularz płatności */}
            <form className="mb-4 rounded bg-white px-8 pt-6 pb-8 shadow-md">
              <div className="mb-4">
                <label
                  className="mb-2 block text-sm font-bold text-gray-700"
                  htmlFor="name"
                >
                  Full Name
                </label>
                <input
                  className="focus:shadow-outline w-full appearance-none rounded border py-2 px-3 leading-tight text-gray-700 shadow focus:outline-none"
                  id="name"
                  type="text"
                  placeholder="John Doe"
                />
              </div>
              <div className="mb-4">
                <label
                  className="mb-2 block text-sm font-bold text-gray-700"
                  htmlFor="card"
                >
                  Credit Card Number
                </label>
                <input
                  className="focus:shadow-outline w-full appearance-none rounded border py-2 px-3 leading-tight text-gray-700 shadow focus:outline-none"
                  id="card"
                  type="text"
                  placeholder="XXXX-XXXX-XXXX-XXXX"
                />
              </div>
              <div className="mb-4">
                <label
                  className="mb-2 block text-sm font-bold text-gray-700"
                  htmlFor="expiry"
                >
                  Expiry Date
                </label>
                <input
                  className="focus:shadow-outline w-full appearance-none rounded border py-2 px-3 leading-tight text-gray-700 shadow focus:outline-none"
                  id="expiry"
                  type="text"
                  placeholder="MM/YYYY"
                />
              </div>
              <div className="mb-4">
                <label
                  className="mb-2 block text-sm font-bold text-gray-700"
                  htmlFor="cvv"
                >
                  CVV
                </label>
                <input
                  className="focus:shadow-outline w-full appearance-none rounded border py-2 px-3 leading-tight text-gray-700 shadow focus:outline-none"
                  id="cvv"
                  type="text"
                  placeholder="XXX"
                />
              </div>
              <div className="flex items-center justify-between">
                <button
                  className="focus:shadow-outline rounded bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700 focus:outline-none"
                  type="button"
                >
                  Pay Now
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default page;
