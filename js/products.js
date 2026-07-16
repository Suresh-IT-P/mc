const products = [
  {
    id: 1,
    name: "Axxis Draken Solid Matte Black Helmet",
    category: "Helmets",
    price: 3850,
    image: "https://images.unsplash.com/photo-1558981806-ec527fa84c39?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    description: "The Axxis Draken helmet offers a sleek matte black finish with superior aerodynamic design and DOT certified safety."
  },
  {
    id: 2,
    name: "Rynox Stealth Evo V3 Riding Jacket",
    category: "Riding Gear",
    price: 6500,
    image: "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    description: "Premium riding jacket with CE Level 2 protectors on shoulders, elbows, and back."
  },
  {
    id: 3,
    name: "Raida Aero Riding Gloves",
    category: "Riding Gear",
    price: 2200,
    image: "https://images.unsplash.com/photo-1518131379650-8b17300c73e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    description: "Mesh and leather hybrid gloves perfect for summer riding with knuckle protection."
  },
  {
    id: 4,
    name: "Bar End Mirrors - Round",
    category: "Accessories",
    price: 850,
    image: "https://images.unsplash.com/photo-1615172282427-9a57ef2d142e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    description: "CNC machined aluminum bar end mirrors for a cafe racer look."
  },
  {
    id: 5,
    name: "MT Thunder 3 Pro Helmet",
    category: "Helmets",
    price: 5200,
    image: "https://images.unsplash.com/photo-1533560904424-a0c61dc306fc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    description: "Sport touring helmet with integrated sun visor and high impact shell."
  },
  {
    id: 6,
    name: "Universal LED Indicators",
    category: "Accessories",
    price: 600,
    image: "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    description: "Bright sequential LED turn signals, universal fit for all motorcycles."
  }
];

// Helper to format currency
function formatPrice(price) {
  return "₹" + price.toLocaleString("en-IN");
}
