class CreateHunches < ActiveRecord::Migration
  def self.up
    create_table :hunches do |t|
      t.string :title
      t.text :description
      t.string :Geographicarea
      t.string :Sector

      t.timestamps
    end
  end

  def self.down
    drop_table :hunches
  end
end