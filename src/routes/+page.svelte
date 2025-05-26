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
</script>

<h2>mc.colonycraft.org</h2>
<div id="controls">
	<label>World X: <input type="number" bind:value={inputX} /></label>
	<label>World Z: <input type="number" bind:value={inputZ} /></label>
	<button on:click={pingCoords}>Ping</button>
</div>
<div id="map-container">
	<img
		id="map"
		bind:this={map}
		src="/earth.png"
		alt="Labeled Map"
		on:mousemove={handleMouseMove}
		on:mouseleave={handleMouseLeave}
	/>
	<div id="coords" bind:this={coordsDiv}></div>
	<div id="ping" bind:this={pingDiv}></div>
</div>
