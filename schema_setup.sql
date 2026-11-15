-- ============================================================================
-- SILENT EXPLORERS: OFF-WORLD MONUMENTS (1960s-PRESENT)
-- Database Setup & Seed Data for Supabase
-- ============================================================================

-- 1. Create artifacts table
CREATE TABLE IF NOT EXISTS public.artifacts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    zone TEXT NOT NULL CHECK (zone IN ('moon', 'mars', 'deep_space')),
    nssdc_link TEXT NOT NULL,
    nasa_description TEXT NOT NULL,
    status TEXT,
    power_source TEXT,
    landing_coordinates TEXT,
    hotspots JSONB DEFAULT '[]'::jsonb,
    first_person_script TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create passport_badges table for tracking student achievements
CREATE TABLE IF NOT EXISTS public.passport_badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    badge_key TEXT NOT NULL,
    badge_name TEXT NOT NULL,
    unlocked_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Enable Row Level Security & Allow Public Read/Write Policies
ALTER TABLE public.artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.passport_badges ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read on artifacts" ON public.artifacts;
CREATE POLICY "Allow public read on artifacts" ON public.artifacts
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Allow public all on passport_badges" ON public.passport_badges;
CREATE POLICY "Allow public all on passport_badges" ON public.passport_badges
    FOR ALL USING (true);

-- 4. Insert the 18 Official NASA Machines (Single Source of Truth)
INSERT INTO public.artifacts (id, name, zone, nssdc_link, nasa_description, status, power_source, landing_coordinates)
VALUES

-- ----------------- THE MOON (4) -----------------
(
    'apollo-lunar-modules',
    'Apollo Lunar Modules',
    'moon',
    'https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-059C',
    'Descent stages (like Apollo 11''s Eagle) were left behind as launch pads.',
    'Left behind as launch pads',
    'Silver-zinc batteries (Descent Stage)',
    '0.67408° N, 23.47297° E (Apollo 11 Eagle)'
),
(
    'lunar-roving-vehicles',
    'Lunar Roving Vehicles (LRVs)',
    'moon',
    'https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1971-063C',
    'Three electric "moon buggies" driven by astronauts. Parked permanently on the Moon.',
    'Parked permanently on the Moon',
    'Non-rechargeable silver-zinc potassium hydroxide batteries (two 36V batteries)',
    '26.13° N, 3.63° E (Apollo 15 site)'
),
(
    'alsep-scientific-packages',
    'ALSEP Scientific Packages',
    'moon',
    'https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-099C',
    'Seismometers, retroreflectors, etc. left to do science after astronauts departed.',
    'Decommissioned in 1977; passive retroreflectors still functional',
    'SNAP-27 Radioisotope Thermoelectric Generator (RTG)',
    NULL
),
(
    'surveyor-landers',
    'Surveyor Landers',
    'moon',
    'https://science.nasa.gov/mission/surveyor-3/',
    '1960s robotic probes sent to prove soft landings were possible.',
    'Inactive / Historic soft-landing monuments',
    'Solar panel + rechargeable silver-zinc batteries',
    '3.015° S, 23.418° W (Surveyor 3)'
),

-- ----------------- MARS (8) -----------------
(
    'sojourner-rover',
    'Sojourner Rover',
    'mars',
    'https://science.nasa.gov/mission/mars-pathfinder/',
    'First rover on Mars (1997), delivered by Pathfinder. Now permanently parked.',
    'Now permanently parked',
    'GaAs solar array + primary non-rechargeable lithium D-cells',
    '19.33° N, 33.55° W (Ares Vallis)'
),
(
    'spirit-rover',
    'Spirit Rover',
    'mars',
    'https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/',
    'Twin rovers that operated for years. Both now inactive.',
    'Inactive (lost contact 2010)',
    'Triple-junction GaAs solar arrays + rechargeable lithium-ion batteries',
    '14.5684° S, 175.4726° E (Gusev Crater)'
),
(
    'opportunity-rover',
    'Opportunity Rover',
    'mars',
    'https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/',
    'Twin rovers that operated for years. Both now inactive.',
    'Inactive (lost in 2018 dust storm)',
    'Triple-junction GaAs solar arrays + rechargeable lithium-ion batteries',
    '1.9483° S, 354.4742° E (Meridiani Planum)'
),
(
    'viking-1-lander',
    'Viking 1 Lander',
    'mars',
    'https://science.nasa.gov/mission/viking-1/',
    'First U.S. landers to successfully operate on Mars (1976), still where they touched down.',
    'Still where they touched down (Silent monument)',
    'SNAP-19 Radioisotope Thermoelectric Generators (2 RTGs)',
    '22.697° N, 48.222° W (Chryse Planitia)'
),
(
    'viking-2-lander',
    'Viking 2 Lander',
    'mars',
    'https://science.nasa.gov/mission/viking-1/',
    'First U.S. landers to successfully operate on Mars (1976), still where they touched down.',
    'Still where they touched down (Silent monument)',
    'SNAP-19 Radioisotope Thermoelectric Generators (2 RTGs)',
    '47.968° N, 225.738° W (Utopia Planitia)'
),
(
    'phoenix-lander',
    'Phoenix Lander',
    'mars',
    'https://science.nasa.gov/mission/insight/',
    'Phoenix dug for water ice; InSight listened for marsquakes. Both lost power.',
    'Lost power (frozen in Martian arctic winter)',
    'Dual circular GaAs solar arrays + lithium-ion batteries',
    '68.2188° N, 234.2508° E (Vastitas Borealis)'
),
(
    'insight-lander',
    'InSight Lander',
    'mars',
    'https://science.nasa.gov/mission/insight/',
    'Phoenix dug for water ice; InSight listened for marsquakes. Both lost power.',
    'Lost power (solar panels covered in dust, Dec 2022)',
    'Dual UltraFlex solar array wings',
    '4.502° N, 135.623° E (Elysium Planitia)'
),
(
    'ingenuity-helicopter',
    'Ingenuity Helicopter',
    'mars',
    'https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/',
    'First aircraft on another planet. Rotor damage, now a stationary artifact.',
    'Rotor damage, now a stationary artifact',
    'Solar panel + 6 Sony lithium-ion cells (350W peak)',
    '18.4446° N, 77.4509° E (Valinor Hills)'
),

-- ----------------- DEEP SPACE (6) -----------------
(
    'dawn-spacecraft',
    'Dawn Spacecraft',
    'deep_space',
    'https://science.nasa.gov/mission/dawn/',
    'Mapped Vesta and Ceres. Out of fuel, in unpowered orbit around Ceres.',
    'Out of fuel, in unpowered orbit around Ceres',
    'Triple-junction solar arrays (10 kW at 1 AU) + Xenon ion propulsion',
    NULL
),
(
    'near-shoemaker',
    'NEAR Shoemaker',
    'deep_space',
    'https://science.nasa.gov/mission/near-shoemaker/',
    'First to orbit and land on an asteroid. Resting on 433 Eros.',
    'Resting on 433 Eros',
    '4 Gallium Arsenide solar panels',
    NULL
),
(
    'pioneer-10',
    'Pioneer 10',
    'deep_space',
    'https://science.nasa.gov/mission/pioneer-10/',
    'Early outer-planet probes, now drifting out of the solar system.',
    'Drifting out of the solar system (Silent interstellar probe)',
    '4 SNAP-19 Radioisotope Thermoelectric Generators (RTGs)',
    NULL
),
(
    'pioneer-11',
    'Pioneer 11',
    'deep_space',
    'https://science.nasa.gov/mission/pioneer-10/',
    'Early outer-planet probes, now drifting out of the solar system.',
    'Drifting out of the solar system (Silent interstellar probe)',
    '4 SNAP-19 Radioisotope Thermoelectric Generators (RTGs)',
    NULL
),
(
    'kepler-space-telescope',
    'Kepler Space Telescope',
    'deep_space',
    'https://science.nasa.gov/mission/kepler/',
    'Exoplanet hunter, out of fuel, drifting in an Earth-trailing orbit.',
    'Out of fuel, drifting in an Earth-trailing orbit',
    'Body-mounted solar arrays + NiCd batteries',
    NULL
),
(
    'voyager-1',
    'Voyager 1',
    'deep_space',
    'https://science.nasa.gov/mission/voyager-1/',
    'Active, still sending signals from interstellar space.',
    'Active, still sending signals from interstellar space',
    '3 Radioisotope Thermoelectric Generators (RTGs)',
    NULL
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    zone = EXCLUDED.zone,
    nssdc_link = EXCLUDED.nssdc_link,
    nasa_description = EXCLUDED.nasa_description,
    status = EXCLUDED.status,
    power_source = EXCLUDED.power_source,
    landing_coordinates = EXCLUDED.landing_coordinates;
