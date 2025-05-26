<script lang="ts">
	import '../app.css';
</script>

<svelte:head>
	<meta charset="UTF-8" />
	<title>Colony Craft Map</title>
	<meta name="description" content="View where you are on Colony Craft!" />

	<!-- Facebook Meta Tags -->
	<meta property="og:url" content="https://github.com/PatatoBit/ColonyCraftMapper" />
	<meta property="og:type" content="website" />
	<meta property="og:title" content="Colony Craft Map" />
	<meta property="og:description" content="View where you are on Colony Craft!" />
	<meta
		property="og:image"
		content="https://opengraph.b-cdn.net/production/images/2c1b86d4-165f-4c8f-8912-65b321c2b3d0.png?token=fQEetdRdSOlidepRSKnY-djFqAgDTTbRWg0Gy1iD-fU&height=600&width=1200&expires=33284247280"
	/>
	<!-- Twitter Meta Tags -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta property="twitter:domain" content="github.com" />
	<meta property="twitter:url" content="https://github.com/PatatoBit/ColonyCraftMapper" />
	<meta name="twitter:title" content="Colony Craft Map" />
	<meta name="twitter:description" content="View where you are on Colony Craft!" />
	<meta
		name="twitter:image"
		content="https://opengraph.b-cdn.net/production/images/2c1b86d4-165f-4c8f-8912-65b321c2b3d0.png?token=fQEetdRdSOlidepRSKnY-djFqAgDTTbRWg0Gy1iD-fU&height=600&width=1200&expires=33284247280"
	/>

	<!-- Meta Tags Generated via https://www.opengraph.xyz -->
	<style>
		body {
			font-family: Arial, sans-serif;
			background: #222;
			color: #eee;
		}
		#map-container {
			position: relative;
			display: inline-block;
			max-width: 100%;
		}
		#map {
			width: 100%;
			height: auto;
			display: block;
			max-width: 100vw;
		}
		#coords {
			position: absolute;
			top: 10px;
			left: 10px;
			background: rgba(0, 0, 0, 0.7);
			padding: 6px 12px;
			border-radius: 6px;
			font-size: 16px;
			pointer-events: none;
			z-index: 2;
		}
		#ping {
			position: absolute;
			width: 16px;
			height: 16px;
			margin-left: -8px;
			margin-top: -8px;
			border: 2px solid #ff0;
			border-radius: 50%;
			background: rgba(255, 255, 0, 0.5);
			pointer-events: none;
			display: none;
			z-index: 2;
		}
		#controls {
			margin: 20px 0;
		}
		label,
		input,
		button {
			font-size: 16px;
		}
		input {
			width: 80px;
		}
	</style>
</svelte:head>

<slot />
