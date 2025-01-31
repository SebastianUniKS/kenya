// const leafletComponent = {
//   template: "<div></div>",
 
//   mounted() {
//       this.map = L.map(this.$el);
//       this.map.addEventListener("click", this.get_location);

//       // Basemaps
//       var basemaps = {
//           OSM: L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png"),
//           Google: L.tileLayer("http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",{
//               maxZoom: 20,
//               subdomains:['mt0','mt1','mt2','mt3']
//           }),
//       };

//       var geoserver = "http://141.51.249.175:8081/geoserver/InfoRange/wms?";
//       var overlay = { 
//           latest_Classification: L.tileLayer.wms(geoserver, {
//               layers: 'latest_classification_amballo',
//               transparent: 'true',
//               format: 'image/png',
//           }),
//           Amballo_2024_Feb: L.tileLayer.wms(geoserver, {
//               layers: 'classified_sololo_20240212',
//               transparent: 'true',
//               format: 'image/png',
//           }),
//       };

//       L.control.layers(basemaps, overlay).addTo(this.map);
//       basemaps.OSM.addTo(this.map);
//       overlay.latest_Classification.addTo(this.map);
//       overlay.Amballo_2024_Feb.addTo(this.map);
//   },
 
//   methods: {
//       set_location(latitude, longitude) {
//           this.target = L.latLng(latitude, longitude);
//           this.map.setView(this.target, 9);
//           if (this.marker) {
//               this.map.removeLayer(this.marker);
//           }
//           this.marker = L.marker(this.target).addTo(this.map);
//       },

//       set_point(x, y) {
//           var goatIcon = L.icon({
//               iconUrl: "/pics/goat.png",
//               iconSize: [38, 38], 
//               iconAnchor: [22, 22], 
//               popupAnchor: [-3, -76] 
//           });
//           L.marker([x, y], {icon: goatIcon}).addTo(this.map);
//       },

//       get_location(e) {
//           var coord = e.latlng;
//           var lat = coord.lat;
//           var lng = coord.lng;
//           console.log("Clicked at:", lat, lng);
//           this.set_point(lat, lng);
//       },
//   },
// };

// // Register the component globally so it can be used in NiceGUI
// window.leafletComponent = leafletComponent;

// window.set_point = function(x, y) {
//   if (leafletComponent.map) {
//       leafletComponent.methods.set_point.call(leafletComponent, x, y);
//   } else {
//       console.error("Map is not initialized yet.");
//   }
// };


export default {
    template: "<div></div>",
   
    mounted() {
        this.map = L.map(this.$el);
        this.map.addEventListener("click", this.get_location)
        // this.get_location()
        window.leafletInstance = this;

    //   basemaps
        var basemaps = {
            OSM: L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png"),
            Google: L.tileLayer("http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",{
                maxZoom: 20,
                subdomains:['mt0','mt1','mt2','mt3']
            }),
        }
    //   geoserver
        var geoserver = "http://141.51.249.175:8081/geoserver/InfoRange/wms?"
        var overlay = { 
            latest_Classification: L.tileLayer.wms(geoserver, {
                layers: 'latest_classification_amballo',
                transparent: 'true',
                format: 'image/png',
            }),
            Amballo_2024_Feb: L.tileLayer.wms(geoserver, {
              layers: 'classified_sololo_20240212',
              transparent: 'true',
              format: 'image/png',
           }),
            // what_is_here: L.tileLayer.wms(geoserver,{
            //     layers: "whats_here",
            //     transparent: 'true',
            //     format: 'image/png',
            // }),
        }

        var pointLayer = {

        }
    
        L.control.layers(basemaps, overlay).addTo(this.map);
    
        basemaps.OSM.addTo(this.map);
        overlay.latest_Classification.addTo(this.map);
        overlay.Amballo_2024_Feb.addTo(this.map);
    

    

    },
   
    methods: {
      set_location(latitude, longitude) {
        this.target = L.latLng(latitude, longitude);
        this.map.setView(this.target, 9);
        if (this.marker) {
          this.map.removeLayer(this.marker);
        }
        this.marker = L.marker(this.target);
        this.marker.addTo(this.map);
      },

      test(){
        console.log('Am I a function?')
      },
      
      set_point(x, y){
        // console.log(x,y)
        // custom icon
        var goatIcon = L.icon({
          iconUrl: "/pics/goat.png",
          iconSize:     [38, 38], // size of the icon
          iconAnchor:   [22, 22], // point of the icon which will correspond to marker's location
          popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
          });
        var new_point = L.marker([x,y], {icon: goatIcon}).addTo(this.map);
        // var new_point = L.marker([x,y]).addTo(this.map);
      },

      async get_location(e){
            var coord = e.latlng;
            var lat = coord.lat;
            var lng = coord.lng;
            console.log("You clicked the map at latitude: " + lat + " and longitude: " + lng);
            this.set_point(lat,lng)
            },
      test(){
        console.log("clicktest")
      }
     },
      
  };

  // Expose set_point globally
window.set_point = function(x, y) {
  if (window.leafletInstance) {
      window.leafletInstance.set_point(x, y);
  } else {
      console.error("Leaflet instance not initialized yet.");
  }
};



  // function getStuff() {
  //   let url = "/api/score"
  //       fetch(url)
  //       .then((response)=>response.json())
  //       .then((data) =>{
  //           console.log(data)
  //         }
  //       )
  //   confirm("data loaded");
  //   // location.reload();
  //   };   