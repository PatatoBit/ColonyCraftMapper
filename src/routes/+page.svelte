<script lang="ts">
	import { onMount } from 'svelte';

	let imgWidth = 0,
		imgHeight = 0;
	let map: HTMLImageElement;
	let coordsDiv: HTMLDivElement;
	let pingDiv: HTMLDivElement;
	let inputX = 0;
	let inputZ = 0;

	// World bounds and scale (must match Python script)
	const world_x_min = -6144,
		world_x_max = 6144;
	const world_z_min = -3072,
		world_z_max = 3072;

	onMount(() => {
		if (map) {
			map.onload = () => {
				imgWidth = map.naturalWidth;
				imgHeight = map.naturalHeight;
			};
		}
	});

	function pixelToWorld(px: number, py: number) {
		const scale_x = (world_x_max - world_x_min) / imgWidth;
		const scale_z = (world_z_max - world_z_min) / imgHeight;
		const wx = Math.round(world_x_min + px * scale_x);
		const wz = Math.round(world_z_min + py * scale_z);
		return { wx, wz };
	}

	function worldToPixel(wx: number, wz: number) {
		const scale_x = (world_x_max - world_x_min) / imgWidth;
		const scale_z = (world_z_max - world_z_min) / imgHeight;
		const px = Math.round((wx - world_x_min) / scale_x);
		const py = Math.round((wz - world_z_min) / scale_z);
		return { px, py };
	}

	function handleMouseMove(e: MouseEvent) {
		const rect = map.getBoundingClientRect();
		const px = Math.floor((e.clientX - rect.left) * (imgWidth / rect.width));
		const py = Math.floor((e.clientY - rect.top) * (imgHeight / rect.height));
		if (px < 0 || py < 0 || px >= imgWidth || py >= imgHeight) {
			coordsDiv.style.display = 'none';
			return;
		}
		const { wx, wz } = pixelToWorld(px, py);
		coordsDiv.textContent = `${wx}, ${wz}`; // Removed pixel coordinates
		coordsDiv.style.display = 'block';
		coordsDiv.style.left = e.clientX - rect.left + 15 + 'px';
		coordsDiv.style.top = e.clientY - rect.top + 15 + 'px';
	}

	function handleMouseLeave() {
		coordsDiv.style.display = 'none';
	}

	function pingCoords() {
		const wx = Number(inputX);
		const wz = Number(inputZ);
		if (isNaN(wx) || isNaN(wz)) return;
		if (imgWidth === 0 || imgHeight === 0) {
			alert('Image not loaded yet.');
			return;
		}
		const { px, py } = worldToPixel(wx, wz);
		if (px < 0 || py < 0 || px >= imgWidth || py >= imgHeight) {
			alert('Coordinates out of bounds.');
			return;
		}
		const rect = map.getBoundingClientRect();
		const scaleX = rect.width / imgWidth;
		const scaleY = rect.height / imgHeight;
		pingDiv.style.left = px * scaleX + 'px';
		pingDiv.style.top = py * scaleY + 'px';
		pingDiv.style.display = 'block';
	}

	const ores = [
		'Acanthite',
		'Coal',
		'Diamond',
		'Gold',
		'Iron',
		'Netherite',
		'Redstone',
		'Valtronium'
	];

	let oreToggles: Record<string, boolean> = {};
	ores.forEach((ore) => (oreToggles[ore] = false));
</script>

<h2>mc.colonycraft.org</h2>
<div id="controls">
	<label>World X: <input type="number" bind:value={inputX} /></label>
	<label>World Z: <input type="number" bind:value={inputZ} /></label>
	<button on:click={pingCoords}>Ping</button>
	<!-- Ores toggles -->
	<div id="ore-toggles">
		{#each ores as ore}
			<label>
				<input type="checkbox" bind:checked={oreToggles[ore]} />
				{ore}
			</label>
		{/each}
	</div>
</div>
<div id="map-container" style="position: relative;">
	<img
		id="map"
		bind:this={map}
		src="/earth.png"
		alt="Labeled Map"
		on:mousemove={handleMouseMove}
		on:mouseleave={handleMouseLeave}
		style="display: block;"
	/>
	<!-- Ore overlays -->
	{#each ores as ore}
		{#if oreToggles[ore]}
			<img
				src={`/ores/${ore}.png`}
				alt={ore}
				style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none;"
			/>
		{/if}
	{/each}
	<div id="coords" bind:this={coordsDiv}></div>
	<div id="ping" bind:this={pingDiv}></div>
</div>

<style>
	#controls {
		background: #222c;
		border-radius: 10px;
		padding: 1rem 1.5rem;
		margin-bottom: 1rem;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 1.5rem;
		box-shadow: 0 2px 8px #0002;
	}

	#controls label {
		font-weight: 500;
		margin-right: 1rem;
		color: #eee;
	}

	#controls input[type='number'] {
		width: 6em;
		padding: 0.2em 0.5em;
		border-radius: 5px;
		border: 1px solid #888;
		background: #222;
		color: #fff;
	}

	#controls button {
		background: #3a6ea5;
		color: #fff;
		border: none;
		border-radius: 5px;
		padding: 0.4em 1.2em;
		font-weight: bold;
		cursor: pointer;
		transition: background 0.2s;
	}
	#controls button:hover {
		background: #29507a;
	}

	#ore-toggles {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5em;
	}

	#ore-toggles label {
		background: #333b;
		border-radius: 6px;
		padding: 0.3em 0.8em 0.3em 0.5em;
		display: flex;
		align-items: center;
		cursor: pointer;
		transition: background 0.2s;
		user-select: none;
	}

	#ore-toggles label:hover {
		background: #3a6ea5bb;
	}

	#ore-toggles input[type='checkbox'] {
		accent-color: #3a6ea5;
		margin-right: 0.4em;
	}

	#map-container {
		border-radius: 10px;
		overflow: hidden;
		box-shadow: 0 2px 12px #0003;
		background: #181818;
		position: relative;
		max-width: 100%;
	}

	#map {
		display: block;
		width: 100%;
		height: auto;
		border-radius: 10px;
	}

	#coords {
		position: absolute;
		pointer-events: none;
		background: #222e;
		color: #fff;
		padding: 0.2em 0.7em;
		border-radius: 5px;
		font-size: 1em;
		font-family: monospace;
		white-space: nowrap;
		z-index: 10;
		border: 1px solid #3a6ea5;
		box-shadow: 0 2px 6px #0004;
	}

	#ping {
		position: absolute;
		width: 18px;
		height: 18px;
		background: #3a6ea5cc;
		border: 2px solid #fff;
		border-radius: 50%;
		transform: translate(-50%, -50%);
		display: none;
		z-index: 20;
		box-shadow: 0 0 8px #3a6ea5cc;
		pointer-events: none;
	}
</style>
